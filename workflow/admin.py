from django.contrib import admin
from django import forms

# Register your models here.
from django.apps import apps

# Get all models from the current app
from .models import *


from django import forms
from django.contrib.admin import ModelAdmin
from .models import Workflow



class WorkflowAdminForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ["request_from_type", 'request_item', "request_quantity", "request_dest_type", "request_from_id", "request_dest_id", 'status', 'bill_image', 'bill_amount', 'purchase_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the choices for request_from_type to include only specific models
        allowed_models = [SiteModel, WarehouseModel, SupplierModel]
        self.fields['request_from_type'].queryset = ContentType.objects.filter(
            model__in=[model._meta.model_name for model in allowed_models]
        )
        self.fields['request_from_type'].label_from_instance = lambda obj: obj.model

        # Filter the choices for request_dest_type to include only specific models
        self.fields['request_dest_type'].queryset = ContentType.objects.filter(
            model__in=[model._meta.model_name for model in allowed_models]
        )
        self.fields['request_dest_type'].label_from_instance = lambda obj: obj.model

    def clean(self):
        cleaned_data = super().clean()
        request_from_type = cleaned_data.get('request_from_type')
        status = cleaned_data.get('status')

        # Check if request_from_type is SupplierModel and enforce required fields
        if request_from_type and request_from_type.model == 'suppliermodel' and status=="completed":
            if not cleaned_data.get('bill_image'):
                self.add_error('bill_image', 'This field is required when request_from_type is SupplierModel.')
            if not cleaned_data.get('bill_amount'):
                self.add_error('bill_amount', 'This field is required when request_from_type is SupplierModel.')
            if not cleaned_data.get('purchase_type'):
                self.add_error('purchase_type', 'This field is required when request_from_type is SupplierModel.')

        # Ensure that once the status is 'completed', it cannot be changed to another status
        if self.instance.status == 'completed' and status != 'completed':
            raise forms.ValidationError("Cannot change status from 'completed' to another status.")

        return cleaned_data

class WorkflowAdmin(admin.ModelAdmin):
    form = WorkflowAdminForm
    change_form_template = 'admin/workflow/workflow/change_form.html'

admin.site.register(Workflow, WorkflowAdmin)

class FuelWorkflowAdminForm(forms.ModelForm):
    class Meta:
        model = FuelWorkflow
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.request_by = self.current_user
        if commit:
            instance.save()
        return instance
class FuelWorkflowAdmin(admin.ModelAdmin):
    form = FuelWorkflowAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.request_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(FuelWorkflow, FuelWorkflowAdmin)
