from django.contrib import admin
from django import forms

# Register your models here.
from django.apps import apps

# Get all models from the current app
from .models import *
# Convert the models to a list



class WorkflowAdminForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ["request_from_type",'request_item',"request_quantity", "request_dest_type","request_from_id","request_dest_id",'status']

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

class WorkflowAdmin(admin.ModelAdmin):
    form = WorkflowAdminForm
    change_form_template = 'admin/workflow/workflow/change_form.html'

admin.site.register(Workflow, WorkflowAdmin)