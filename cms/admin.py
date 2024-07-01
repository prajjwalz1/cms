from django.contrib import admin
from cms.models import *
from users.models import *
admin.site.register(CategoryModel)
admin.site.register(BrandModel)
admin.site.register(SupplierModel)
admin.site.register(WarehouseModel)
admin.site.register(ItemModel)
admin.site.register(VehicleModel)
admin.site.register(SiteModel)
admin.site.register(GroupModel)
admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(ItemUnit)
admin.site.register(VehicleWorkLogs)
admin.site.register(Manpower)
