
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


class RequestWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'
        read_only_fields = ['status']  # Make the status field read-only

    def to_representation(self, instance):
        ret= super().to_representation(instance)
        request_from_model=instance.request_from_type.model
        print(request_from_model)
        if request_from_model:
            ret['request_from_type']=str(request_from_model)
        return ret

    def validate(self, data):
        # Call the default model validation
        data = super().validate(data)
        request_from_type = data.get('request_from_type')
        
        if request_from_type and request_from_type.model == 'suppliermodel' and data.get("status") in ["approved","completed"]:
            if not data.get('bill_image'):
                raise serializers.ValidationError({'bill_image': 'This field is required when request_from_type is supplier.'})
            if not data.get('bill_amount'):
                raise serializers.ValidationError({'bill_amount': 'This field is required when request_from_type is supplier.'})
            if not data.get('purchase_type'):
                raise serializers.ValidationError({'purchase_type': 'This field is required when request_from_type is supplier.'})

        # Return the validated data
        return data
    

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