# inventory/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from workflow.models import Workflow
from .models import SiteInventory, SiteInventoryDetails, WareHouseInventory, WareHouseInventoryDetails,SupplierModel
from account.models import CreditRecord
@receiver(post_save, sender=Workflow)
def update_inventory(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.request_item and instance.request_quantity:
        # Handle decreasing quantity from request_from inventory
        if instance.request_from_type.model == 'sitemodel':
            print(instance.request_from_id,"request-id")
            site_inventory, created = SiteInventory.objects.get_or_create(
                site_id=instance.request_from_id)
            print(site_inventory)

            inventory_detail,created = SiteInventoryDetails.objects.get_or_create(
                site_inventory=site_inventory,
                item=instance.request_item
            )

            inventory_detail.quantity -= instance.request_quantity
            inventory_detail.save()
        
        elif instance.request_from_type.model == 'warehousemodel':
            print("from warehouse model")
            inventory_detail,created = WareHouseInventoryDetails.objects.get_or_create(
                warehouse_inventory__warehouse__id=instance.request_from_id,
                item=instance.request_item
            )
            inventory_detail.quantity -= instance.request_quantity
            inventory_detail.save()

        elif instance.request_from_type.model == 'suppliermodel':
            # Create or update SupplierModel and CreditRecord
            supplier, created = SupplierModel.objects.get_or_create(id=instance.request_from_id)
            if instance.purchase_type == 'credit':
                CreditRecord.objects.create(
                    supplier=supplier,
                    credit_amount=instance.bill_amount,
                    # Add other fields as needed
                )

        # Handle increasing quantity in request_dest inventory
        if instance.request_dest_type.model == 'sitemodel':
            print("to site model",instance.request_dest_id)
            siteinventory, created = SiteInventory.objects.get_or_create(
                site__id=instance.request_dest_id,
            )
            print("dest site model",SiteInventory)
            dest_inventory, created = SiteInventoryDetails.objects.get_or_create(
                site_inventory=siteinventory,
                item=instance.request_item,
            )
            dest_inventory.quantity += int(instance.request_quantity)
            dest_inventory.save()
        
        elif instance.request_dest_type.model == 'warehousemodel':
            warehouse_inventory, created = WareHouseInventory.objects.get_or_create(
                warehouse_id= instance.request_dest_id
            )
            print(warehouse_inventory)
            dest_inventory, created = WareHouseInventoryDetails.objects.get_or_create(
                warehouse_inventory=warehouse_inventory,
                item=instance.request_item,
            )
            print(dest_inventory)
            dest_inventory.quantity += int(instance.request_quantity)
            dest_inventory.save()
