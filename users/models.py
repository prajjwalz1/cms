from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from cms.mixins import *

# from workflow.models import *
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Use auto_now_add for created_at
    phone = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Hash password if not already hashed (i.e., plain-text)
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class PerformanceLogs(DateTimeModel):
    user=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,null=True,blank=True)
    activity=models.CharField(null=True,blank=True)
    updated_by=models.IntegerField(null=True,blank=True)
    # reference=models.ForeignKey(Workflow,on_delete=models.SET_NULL,null=True,blank=True) 
    def __str__(self) -> str:
        return self.activity

class UserPerfomance(DateTimeModel):
    user=models.OneToOneField(CustomUser,on_delete=models.DO_NOTHING,null=True,blank=True)
    score=models.IntegerField(null=True,blank=True,default=0)
    scorelogs=models.ManyToManyField(PerformanceLogs)