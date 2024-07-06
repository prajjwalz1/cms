from django.db import models
from cms.mixins import *
from cms.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Workflow(models.Model):
    request_from_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='request_from_set')
    request_from_id = models.PositiveIntegerField()
    request_from = GenericForeignKey('request_from_type', 'request_from_id')
    request_dest_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='request_dest_set')
    request_dest_id = models.PositiveIntegerField(null=True)
    request_dest = GenericForeignKey('request_dest_type', 'request_dest_id')
    status = models.CharField(choices=(('pending', 'pending'), ('approved', 'approved'), ('completed', 'completed')), default='pending')
    request_item = models.ForeignKey(ItemModel, on_delete=models.SET_NULL, null=True, blank=True)
    request_quantity = models.FloatField(null=True, blank=True)
    bill_image=models.ImageField(upload_to='static/bills',null=True,blank=True)
    bill_amount=models.FloatField(null=True,blank=True)
    purchase_type=models.CharField(choices=(('cash','cash'),('cheque','cheque'),('credit','credit'),('mobile-banking','mobile-banking')),null=True,blank=True)

    def __str__(self):
        if self.request_from and self.request_dest:
            return f"{self.request_quantity} * {self.request_item} from {self.request_from.name} to {self.request_dest.name}" if self.request_from_type.model and self.request_dest_type.model in ["suppliermodel","warehousemodel","sitemodel"] else "None"
        return "Unknown"

    def save(self, *args, **kwargs):
        if self.pk:
            previous = Workflow.objects.get(pk=self.pk)
            if previous.status == 'completed' and self.status != 'completed':
                raise ValueError("Cannot change status from 'completed' to another status")
        super().save(*args, **kwargs)        




class FuelWorkflow(DateTimeModel):
    vehicle=models.ForeignKey(VehicleModel,on_delete=models.SET_NULL,null=True,blank=True)
    remaining_fuel = models.DecimalField(max_digits=10, decimal_places=2)
    request_fuel = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=(
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('completed', 'completed')
        ),
        default='pending'
    )

