from django.urls import path
from .views import *
urlpatterns = [
    path("getinventory/",Inventory.as_view())
]
