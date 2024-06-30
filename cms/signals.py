# Import necessary modules at the top of your models.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
# Assuming your models are defined as previously shown...

@receiver(post_save, sender=VehicleWorkLogs)
def update_current_meter(sender, instance, created, **kwargs):
    if created:  # Only update current meter if a new instance was created
        vehicle = instance.vehicle
        if vehicle:
            # Get the latest VehicleWorkLogs for the same vehicle
            # latest_work_log = VehicleWorkLogs.objects.filter(vehicle=vehicle).order_by('-id').first()
            # if latest_work_log:
                # Update current meter based on the latest work log and the current instance
            vehicle.current_meter += instance.distance_travelled
            vehicle.save()