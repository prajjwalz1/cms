
from rest_framework import serializers
from .models import *
class WorkflowSerializer(serializers.ModelSerializer):
    request_from_type = serializers.CharField(source='request_from_type.model')
    request_dest_type = serializers.CharField(source='request_dest_type.model', allow_null=True)
    request_item = serializers.CharField(source='request_item.name', allow_null=True)
    request_item_unit = serializers.CharField(source='request_item.unit', allow_null=True,)
    request_by=serializers.CharField(source='request_by.contact',allow_null=True)
    class Meta:
        model = Workflow
        fields = ['id','request_item','request_by','request_quantity','request_item_unit', 'request_from_type', 'request_dest_type','status','bill_image','bill_amount','purchase_type']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        
        request_from_instance = instance.request_from
        if request_from_instance:
            ret['request_from'] = str(request_from_instance)
        else:
            ret['request_from'] = None

        request_dest_instance = instance.request_dest
        if request_dest_instance:
            ret['request_dest'] = str(request_dest_instance)
        else:
            ret['request_dest'] = None
        
        return ret

class RequestItemDetailsSerializer(serializers.ModelSerializer):
    items = serializers.IntegerField()

    class Meta:
        model = RequestItemDetails
        fields = ["items", 'request_quantity', 'purpose', 'within']

class RequestWorkflowSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.IntegerField(), write_only=True)  # List of item IDs
    itemsdetails = RequestItemDetailsSerializer(many=True,write_only=True)

    class Meta:
        model = Workflow
        fields = '__all__'
        read_only_fields = ['status']

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Handle request_from_type safely
        try:
            request_from_model = instance.request_from_type.model
            if request_from_model:
                ret['request_from_type'] = str(request_from_model)
        except AttributeError:
            ret['request_from_type'] = None

        # Handle items safely
        try:
            ret['items'] = [item.id for item in instance.items.all()]
        except Exception:
            ret['items'] = []

        return ret

    def validate(self, data):
        data = super().validate(data)
        request_from_type = data.get('request_from_type')

        if request_from_type and request_from_type.model == 'suppliermodel' and data.get("status") in ["approved", "completed"]:
            if not data.get('bill_image'):
                raise serializers.ValidationError({'bill_image': 'This field is required when request_from_type is supplier.'})
            if not data.get('bill_amount'):
                raise serializers.ValidationError({'bill_amount': 'This field is required when request_from_type is supplier.'})
            if not data.get('purchase_type'):
                raise serializers.ValidationError({'purchase_type': 'This field is required when request_from_type is supplier.'})

        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        items_details_data = validated_data.pop("itemsdetails", [])

        # Create the Workflow instance
        workflow = Workflow.objects.create(**validated_data)

        # Handle the many-to-many relationship through RequestItemDetails
        for item_detail_data in items_details_data:
            item_id = item_detail_data.pop('items')
            item_instance = ItemModel.objects.get(id=item_id)
            RequestItemDetails.objects.create(wflow=workflow, items=item_instance, **item_detail_data)

        # Set the many-to-many field
        workflow.items.set(items_data)

        return workflow

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        items_details_data = validated_data.pop('itemsdetails', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Clear existing request items
        if items_data is not None:
            instance.items.clear()
            # Add new request items
            for item_id in items_data:
                item_instance = ItemModel.objects.get(id=item_id)
                instance.items.add(item_instance)

        # Handle itemsdetails
        if items_details_data:
            # Clear existing request item details
            RequestItemDetails.objects.filter(wflow=instance).delete()
            for item_detail_data in items_details_data:
                item_id = item_detail_data.pop('items')
                item_instance = ItemModel.objects.get(id=item_id)
                RequestItemDetails.objects.create(wflow=instance, items=item_instance, **item_detail_data)

        return instance

class RequestFuelSerializer(serializers.ModelSerializer):
    class Meta:
        model=FuelWorkflow
        fields="__all__"


class ApproveWorkflowSerializer(serializers.Serializer):
    workflow_id = serializers.IntegerField()
    bill_amount = serializers.FloatField(required=True) 
    bill_image = serializers.ImageField(required=True)

    def validate(self, data):
        return data