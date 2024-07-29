from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import FuelWorkflow,Workflow


@receiver(post_save, sender=FuelWorkflow)
def send_new_fuel_request_email(sender, instance, created, **kwargs):
    if created:
        print("signals trigerred")
        subject = 'New Fuel Request Created'
        message = f'A new fuel request has been created.\n\nDetails:\nVehicle: {instance.vehicle}\nFuel Quantity: {instance.quantity}\nPurpose: {instance.purpose}'
        from_email = settings.EMAIL_HOST_USER
        to_email = ['samsherthapa91@gmail.com']  # Replace with your recipient's email address
        send_mail(subject, message, from_email, to_email)

@receiver(post_save, sender=FuelWorkflow)
def send_approved_fuel_request_email(sender, instance, created, **kwargs):
    if not created and instance.status == 'approved':
        print("signals trigerred")

        subject = 'Fuel Request Approved'
        message = f'Your fuel request has been approved.\n\nDetails:\nVehicle: {instance.vehicle}\nFuel Quantity: {instance.quantity}\nPurpose: {instance.purpose}\nDownload Coupon: {instance.pdf_link}'
        from_email = settings.EMAIL_HOST_USER
        print(instance.request_by)
        to_email = [instance.request_by.email]  # Assuming request_by is a User model field
        print(to_email)
        send_mail(subject, message, from_email, to_email)

from .models import Workflow, RequestItemDetails
from django.db.models.signals import m2m_changed



@receiver(post_save, sender=Workflow)
def generalworkflow_request_email(sender, instance, created, **kwargs):
    if created:
        print("Signal triggered")
        subject = 'New Workflow Request'
        
        # Build the message with item details
        items_details = []
        for item_detail in RequestItemDetails.objects.filter(wflow=instance):
            item_name = item_detail.items.name
            quantity = item_detail.request_quantity
            purpose = item_detail.purpose
            item_info = f"Item: {item_name}, Quantity: {quantity}, Purpose: {purpose}"
            items_details.append(item_info)
        
        items_details_str = "\n".join(items_details)
        message = f'New workflow has been requested.\n\nDetails:\n{items_details_str}'
        
        from_email = settings.EMAIL_HOST_USER
        to_email = ['samsherthapa91@gmail.com']  # Replace with your recipient's email address
        
        send_mail(subject, message, from_email, to_email)