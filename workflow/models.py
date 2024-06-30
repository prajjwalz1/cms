from django.db import models
from cms.mixins import *
from cms.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Workflow(DateTimeModel):
    request_from_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='request_from_set')
    request_from_id = models.PositiveIntegerField()
    request_from = GenericForeignKey('request_from_type', 'request_from_id')
    request_dest_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='request_dest_set')
    request_dest_id = models.PositiveIntegerField(null=True)
    request_dest = GenericForeignKey('request_dest_type', 'request_dest_id')
    status=models.CharField(choices=(('pending','pending'),('approved','approved'),('completed','completed')),default='pending')
    request_item=models.ForeignKey(ItemModel,on_delete=models.SET_NULL,null=True,blank=True)
    request_quantity=models.FloatField(null=True,blank=True)
    def __str__(self):
        if self.request_from and self.request_dest:
            return f"{self.request_quantity} * {self.request_item} from {self.request_from.name} to {self.request_dest.name}"
        return "Unknown"