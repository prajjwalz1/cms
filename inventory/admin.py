from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(SiteInventory)
admin.site.register(SiteInventoryDetails)
admin.site.register(WareHouseInventory)
admin.site.register(WareHouseInventoryDetails)