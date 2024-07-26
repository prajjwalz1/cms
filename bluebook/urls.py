from django.urls import path
from .views import *
urlpatterns=[

path("bluebook-renew/", vehicle_form, name="vehicle_form"),
]