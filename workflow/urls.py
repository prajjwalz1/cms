from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("request/", WorkflowRequest.as_view(), name="WorkflowRequest"),
    path('get_objects/', get_objects, name='get_objects'),
    path('workflowrequest/', WorkflowRequest.as_view(), name='WorkflowRequest')
]