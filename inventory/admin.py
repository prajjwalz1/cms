from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(SiteInventory)
# admin.site.register(SiteInventoryDetails)
# admin.site.register(WareHouseInventory)
# admin.site.register(WareHouseInventoryDetails)
from collections import defaultdict
from django.contrib import admin
from django.shortcuts import render
from .models import SiteInventory
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
        obj = self.get_object(request, object_id)

        # Aggregate quantities by item
        aggregated_items = defaultdict(int)
        for detail in obj.siteinventorydetails_set.all():
            aggregated_items[detail.item] += detail.quantity

        # Prepare the aggregated data for the template
        aggregated_details = [
            {'item': item, 'quantity': quantity}
            for item, quantity in aggregated_items.items()
        ]

        extra_context['aggregated_details'] = aggregated_details
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
    
@admin.register(SiteInventoryDetails)
class SiteInventoryDetailsAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'site_inventory','updated_at')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(WareHouseInventoryDetails)
class WareHouseInventoryDetailsAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'warehouse_inventory','updated_at')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False