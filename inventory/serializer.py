from rest_framework import serializers
from .models import *
from cms.serializers import SiteModelSerializer,WarehouseModelSerializer
from cms.serializers import ItemModelSerializer


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