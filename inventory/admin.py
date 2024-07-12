from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(SiteInventory)
# admin.site.register(SiteInventoryDetails)
# admin.site.register(WareHouseInventory)
# admin.site.register(WareHouseInventoryDetails)

class SiteInventoryDetailsInline(admin.TabularInline):
    model = SiteInventoryDetails
    extra = 1  # Number of empty forms to display

@admin.register(SiteInventory)
class SiteInventoryAdmin(admin.ModelAdmin):
    list_display = ('site',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('site',)  # Ensure 'site' field is readonly

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_template'] = 'admin/inventory/siteinventory/change_form.html'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    

@admin.register(WareHouseInventory)
class WareHouseInventoryAdmin(admin.ModelAdmin):
    list_display = ('warehouse',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('warehouse',)  # Ensure 'warehouse' field is readonly

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_template'] = 'admin/inventory/warehouseinventory/change_form.html'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)