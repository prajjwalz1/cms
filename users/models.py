from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    name=models.CharField(max_length=255,null=True,blank=True)
    contact = models.CharField(max_length=255, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    phone=models.CharField(null=True,blank=True)

    def __str__(self):
        return self.username
