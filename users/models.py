from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# Create your models here.


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None or 'password' in self.get_deferred_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username