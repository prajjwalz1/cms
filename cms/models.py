from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django.db import models
# from companies.models import Client
from users.models import *
from cms.mixins import *
from django.utils.translation import gettext_lazy as _


# @admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ["name"]


# --------------------------- Construction Management System --------------------------------


class CategoryModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class BrandModel(DateTimeModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class SupplierModel(DateTimeModel):
    name = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=100,null=False,blank=False,default="980000000")
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class WarehouseModel(DateTimeModel):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="warehouse/", blank=True, null=True)
    contact_person = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class ItemUnit(models.Model):
    unit=models.CharField(max_length=255,null=False,blank=False)

    def __str__(self) -> str:
        return self.unit

class ItemModel(DateTimeModel):
    PRODUCT_TYPE_CHOICES = (
        ("Machinery", "Machinery"),
        ("Equipments", "Equipments"),
        ("TransportMaterials", "Transport Materials"),
        ("ConstructionMaterials", "Construction Materials"),
    )

    name = models.CharField(max_length=255,null=False,blank=False,default="test")
    unit=models.ForeignKey(ItemUnit,on_delete=models.SET_NULL,null=True,blank=False)
    category = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING,null=False,blank=False,default="test")
    type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES,null=False,blank=False,default="test")
    brand = models.ForeignKey(
        BrandModel, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    # warehouse = models.ForeignKey(
    #     WarehouseModel, on_delete=models.DO_NOTHING, null=False,blank=False,default=1)
    tax = models.DecimalField(decimal_places=2, max_digits=3, blank=True, null=True)
    image = models.ImageField(upload_to="product/", blank=True, null=True)
    stock_alert=models.IntegerField(default=100)
    def __str__(self) -> str:
        return self.name + " "+'('+self.unit.unit+")" if self.unit else self.name

class VehicleType(DateTimeModel):
    name=models.CharField(max_length=255,null=True,blank=True)

    def __str__(self) -> str:
        return self.name

class VehicleModel(DateTimeModel):
    type = models.ForeignKey(VehicleType, verbose_name=_("vehicle"), on_delete=models.DO_NOTHING)
    vehicle_number = models.CharField(max_length=255)
    contact_person = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    image = models.ImageField(upload_to="vehicle/", blank=True, null=True)
    current_meter=models.IntegerField(null=False,blank=False,default=0)
    last_service_date=models.DateField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.vehicle_number if self.vehicle_number else "None"

class VehicleWorkLogs(DateTimeModel):
    vehicle=models.ForeignKey(VehicleModel,on_delete=models.SET_NULL,null=True,blank=True)
    travel_details=models.TextField(null=True,blank=True)
    worklog_updated=models.DateField(auto_now=True)
    distance_travelled = models.IntegerField(_("Distance Travelled in KM"), null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.vehicle.vehicle_number}travelled {self.distance_travelled}" if self.vehicle else "None"

class VehicleParts(DateTimeModel):
    part_types_choices=(('durable','durable'),('non-durable',('non-durable')))
    parts_name=models.CharField(max_length=255)
    parts_materials_type=models.CharField(choices=part_types_choices)
    parts_quality_type=models.CharField(choices=(('genuine','genuine'),('local','local')))
    parts_price=models.FloatField(null=True,blank=True)
    parts_image=models.ImageField(null=True,blank=True)

    def __str__(self) -> str:
        return self.parts_name


class VehicleServiceLogs(DateTimeModel):
    vehicle=models.ForeignKey(VehicleModel,on_delete=models.SET_NULL,null=True,blank=True)
    service_type=models.CharField(choices=(('servicing','servicing'),('parts_replace','parts_replace'),))
    replace_parts=models.ManyToManyField(VehicleParts,through='partsreplacedetails')
    quatation=models.FileField(upload_to='static/documents/repair/quatations')
    minimium_quation_amount=models.FloatField(null=False,blank=False)
    def __str__(self) -> str:
        return f"{self.vehicle.vehicle_number}travelled {self.distance_travelled}"

class PartsReplaceDetails(DateTimeModel):
    service_log=models.ForeignKey(VehicleServiceLogs,null=True,blank=True,on_delete=models.SET_NULL)
    replace_parts=models.ForeignKey(VehicleParts,null=False,blank=False,on_delete=models.DO_NOTHING)
    replace_date=models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.replace_date
    

class Project(DateTimeModel):
    project_name=models.CharField(max_length=255,null=False,blank=False)
    project_estimation_cost=models.FloatField(null=True,blank=True)
    project_location=models.CharField(null=True,blank=True)
    project_start_date=models.DateField(null=True,blank=True)
    project_dead_line=models.DateField(null=True,blank=True)
    project_progress=models.CharField(max_length=255,null=True,blank=True)
    project_manager=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING, null=True,blank=True)

    def __str__(self) -> str:
        return self.project_name
    
class Document(models.Model):
    project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE)
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to="static/documents/files", null=True,blank=True)
    document_image = models.ImageField(upload_to='static/documents/image',null=True,blank=True)

    def __str__(self):
        return self.document_name
    
class SiteModel(DateTimeModel):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="site/", blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    contact_person = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    project=models.ForeignKey(Project,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self) -> str:
        return self.name

class Manpower(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    position=models.CharField(max_length=255,null=True,blank=True)
    manpower_type=models.CharField(choices=(('skilled','skilled'),('semi-skilled','semi-skilled'),('un-skilled','un-skilled')))
    paymode=models.CharField(choices=(('daily-wages','daily-wages'),('salaried','salaried'),('contract','contract')))
    salary_amount=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    def __str__(self) -> str:
        return self.name
    
class GroupModel(DateTimeModel):
    name = models.CharField(max_length=255, unique=True)
    site = models.ForeignKey(SiteModel,null=True,blank=True,on_delete=models.DO_NOTHING)
    manpower=models.ManyToManyField(Manpower)

    def __str__(self) -> str:
        return self.name


