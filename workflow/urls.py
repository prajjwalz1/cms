from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path("request/", WorkflowRequest.as_view(), name="WorkflowRequest"),
    path('get_objects/', get_objects, name='get_objects'),
    path('workflowrequest/', WorkflowRequest.as_view(), name='WorkflowRequest'),
    path('fuelworkflowrequest/', WorkflowRequest.as_view(), name='WorkflowRequest'),
    path('getcontenttype/', ContentTypeListView.as_view(), name='ContentTypeListView'),
    path('createfuelcoupon/<int:fuel_workflow_id>', views.generate_fuel_workflow_report, name='generate_fuel_workflow_report')
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)