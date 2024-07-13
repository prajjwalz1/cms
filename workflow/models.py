from django.db import models
from cms.mixins import *
from cms.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.
import platform
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
            return f" Status {self.status} for {self.request_quantity} * {self.request_item} from {self.request_from.name} to {self.request_dest.name}" if self.request_from_type.model and self.request_dest_type.model in ["suppliermodel","warehousemodel","sitemodel"] else "None"
        return "Unknown"

    def save(self, *args, **kwargs):
        if self.pk:
            previous = Workflow.objects.get(pk=self.pk)
            if previous.status == 'completed' and self.status != 'completed':
                raise ValueError("Cannot change status from 'completed' to another status")
        super().save(*args, **kwargs)        




class FuelWorkflow(models.Model):
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True, blank=True)
    fuel_supplier = models.ForeignKey(SupplierModel, on_delete=models.SET_NULL, null=True, blank=True)
    fuel_rate = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_fuel = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    purpose = models.CharField(max_length=255, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    request_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True)  # Assuming request_by is a User
    status = models.CharField(
        max_length=10,
        choices=(
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('completed', 'Completed'),
        ),
        default='pending'
    )
    fuel_type = models.CharField(
        max_length=10,
        choices=(
            ('diesel', 'Diesel'),
            ('petrol', 'Petrol'),
        ),
        default='diesel'
    )
    pdf_link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # Calculate total_amount if quantity or fuel_rate has changed
        if self.quantity is not None and self.fuel_rate is not None:
            if self.pk is None or (self.pk is not None and (self.quantity != self.__class__.objects.get(pk=self.pk).quantity or self.fuel_rate != self.__class__.objects.get(pk=self.pk).fuel_rate)):
                self.total_amount = self.quantity * self.fuel_rate

        # Set pdf_link when status changes to 'approved'
        if self.status in ['approved', 'completed'] and not self.pdf_link:
            # Construct the full URL manually based on your project's configuration
            if platform.system() == 'Windows':
                base_url = 'http://localhost:8000'
            elif platform.system() == 'Linux':
                base_url = 'https://kailashcms.carringmanagement.com.au'
            pdf_url = reverse('generate_fuel_workflow_report', args=[self.pk])
            self.pdf_link = base_url + pdf_url
        super().save(*args, **kwargs)

        # Handle sending emails
        # if kwargs.get('send_email', True):
        #     if self.pk is None:  # New instance created
        #         subject = 'New Fuel Request Created'
        #         message = f'A new fuel request has been created.\n\nDetails:\nVehicle: {self.vehicle}\nFuel Quantity: {self.quantity}\nPurpose: {self.purpose}'
        #         from_email = settings.EMAIL_HOST_USER
        #         to_email = ['samsherthapa91@gmail.com']  # Replace with your recipient's email address
        #         send_mail(subject, message, from_email, to_email)
        #     elif self.status == 'approved':  # Request approved
        #         subject = 'Fuel Request Approved'
        #         message = f'Your fuel request has been approved.\n\nDetails:\nVehicle: {self.vehicle}\nFuel Quantity: {self.quantity}\nPurpose: {self.purpose}'
        #         from_email = settings.EMAIL_HOST_USER
        #         to_email = [self.request_by.email]  # Send email to the requester
        #         send_mail(subject, message, from_email, to_email)

    def __str__(self):
        return self.vehicle.vehicle_number