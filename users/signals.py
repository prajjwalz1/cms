from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser
@receiver(pre_save, sender=CustomUser)
def hash_password(sender, instance, **kwargs):
    if instance.pk:  # Existing user instance being updated
        original_instance = sender.objects.get(pk=instance.pk)
        if instance.password != original_instance.password:
            instance.password = make_password(instance.password)