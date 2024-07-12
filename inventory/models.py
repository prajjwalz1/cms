from django.db import models
from cms.mixins import *
from cms.models import *
from django.core.exceptions import ValidationError

# Create your models here.
class SiteInventory(DateTimeModel):
    site = models.ForeignKey(SiteModel, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(ItemModel, through='SiteInventoryDetails')

    def __str__(self):
        return f"Inventory for {self.site}"

    def delete(self, *args, **kwargs):
        raise ValidationError("Deleting SiteInventory instances is not allowed.")


class SiteInventoryDetails(DateTimeModel):
    site_inventory=models.ForeignKey(SiteInventory,on_delete=models.SET_NULL,null=True,blank=True)
    item=models.ForeignKey(ItemModel,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False,default=0)

    def __str__(self):
        return f"{self.quantity} {self.item.unit} {self.item.name}"


class WareHouseInventory(DateTimeModel):
    warehouse=models.ForeignKey(WarehouseModel,on_delete=models.SET_NULL,null=True,blank=True)
    items=models.ManyToManyField(ItemModel,through='WareHouseInventoryDetails')

    def __str__(self):
        return f"Inventory for {self.warehouse}"


class WareHouseInventoryDetails(DateTimeModel):
    warehouse_inventory=models.ForeignKey(WareHouseInventory,on_delete=models.SET_NULL,null=True,blank=True)
    item=models.ForeignKey(ItemModel,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False,default=0)

    def __str__(self):
        return f"{self.item} - {self.quantity}"