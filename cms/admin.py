from django.contrib import admin
from cms.models import *
from users.models import *
admin.site.register(CategoryModel)
admin.site.register(BrandModel)
admin.site.register(SupplierModel)
admin.site.register(WarehouseModel)
admin.site.register(ItemModel)
admin.site.register(VehicleModel)
admin.site.register(VehicleType)
admin.site.register(GroupModel)
admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(ItemUnit)
admin.site.register(VehicleWorkLogs)
admin.site.register(Manpower)
admin.site.register(VehicleParts)
admin.site.register(VehicleServiceLogs)

@admin.register(SiteModel)
class SiteModelAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False