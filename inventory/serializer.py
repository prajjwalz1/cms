from rest_framework import serializers
from .models import *
from cms.serializers import SiteModelSerializer,WarehouseModelSerializer
from cms.serializers import ItemModelSerializer
from workflow.models import *
from users.models import *
class SiteInventoryDetailsSerialzier(serializers.ModelSerializer):
    item_id=serializers.CharField(source='item.id')
    item=serializers.CharField(source='item.name')
    item_unit=serializers.CharField(source='item.unit.unit',allow_null=True)
    low_status=models.BooleanField(default=False)
    class Meta:
        model=SiteInventoryDetails
        fields=['item_id','item','item_unit','quantity']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.item and instance.quantity <= instance.item.stock_alert:
            data['low_status'] = True
        else:
            data['low_status']= False
        current_site = instance.site_inventory.site
        if data['low_status']:
            pending_workflows = Workflow.objects.filter(
                request_dest_id=current_site.id,
                items=instance.item,
                status="pending"
            )
            
            if pending_workflows.exists():
                logs_entry=PerformanceLogs.objects.create(user=current_site.project.project_manager,activity=f"Request workflow for {instance.item} in {current_site.name}",updated_by=5)
                userperformance,create=UserPerfomance.objects.get_or_create(user=current_site.project.project_manager)
                userperformance.score+=5
                userperformance.scorelogs.add(logs_entry)
                userperformance.save()
                print(UserPerfomance)
                data['request'] = {"status":"pending","message":f"{current_site.name} has Pending workflow request to be appoved"}
                
            else:
                data['request'] = {"status":"Alert","message":f'The inventory is Low for {instance.item} in {current_site.name} but has not received the workflow request'}
        else:
            data['request'] = "No action needed"
        data["progress"]=current_site.project.project_progress
        return data

class WarehouseInventorydetailsSerialzier(serializers.ModelSerializer):
    item_id=serializers.CharField(source='item.id')
    item=serializers.CharField(source='item.name')
    item_unit=serializers.CharField(source='item.unit.unit',allow_null=True)
    low_status=models.BooleanField(default=False)
    class Meta:
        model=WareHouseInventoryDetails
        fields=['item_id','item','item_unit','quantity']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.item and instance.quantity <= instance.item.stock_alert:
            data['low_status'] = True
        else:
            data['low_status']= False
        current_warehouse = instance.warehouse_inventory.warehouse
        if data['low_status']:
            pending_workflows = Workflow.objects.filter(
                request_dest_id=current_warehouse.id,
                items=instance.item,
                status="pending"
            )

            if pending_workflows.exists():
                    data['request'] = {"status":"pending","message":f"{current_warehouse.name} Pending workflow request to be appoved"}
            else:
                data['request'] = {"status":"Alert","message":f'The inventory is Low for {instance.item} in {current_warehouse.name} but has not received the workflow request'}
        else:
            data['request'] = {"status":"Ok","message":""}
        # print(pending_workflows.item,".................")
        return data

class SiteInventorySerialzier(serializers.ModelSerializer):
    site=SiteModelSerializer()
    items=SiteInventoryDetailsSerialzier(many=True,source='siteinventorydetails_set')
    class Meta:
        model=SiteInventory
        fields=["site",'items']

class warehouseInventorySerialzier(serializers.ModelSerializer):
    warehouse=WarehouseModelSerializer()
    items=WarehouseInventorydetailsSerialzier(many=True,source='warehouseinventorydetails_set')
    class Meta:
        model=WareHouseInventory
        fields='__all__'