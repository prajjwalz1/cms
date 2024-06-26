from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django.db import models
# from companies.models import Client
from users.models import *
from cms.mixins import *


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
    phone = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
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


class ProductModel(DateTimeModel):
    PRODUCT_TYPE_CHOICES = (
        ("Machinery", "Machinery"),
        ("Equipments", "Equipments"),
        ("TransportMaterials", "Transport Materials"),
        ("ConstructionMaterials", "Construction Materials"),
    )

    name = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES)
    brand = models.ForeignKey(
        BrandModel, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    warehouse = models.ForeignKey(
        WarehouseModel, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    tax = models.DecimalField(decimal_places=2, max_digits=3, blank=True, null=True)
    image = models.ImageField(upload_to="product/", blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class VehicleModel(DateTimeModel):
    VEHICLE_TYPE_CHOICES = (
        ("Truck", "Truck"),
        ("Jeep", "Jeep"),
    )
    vehicle_number = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=VEHICLE_TYPE_CHOICES)
    contact_person = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    image = models.ImageField(upload_to="vehicle/", blank=True, null=True)

    def __str__(self) -> str:
        return self.name


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
    budget_allocation = models.DecimalField(
        decimal_places=2, max_digits=3, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name


class GroupModel(DateTimeModel):
    name = models.CharField(max_length=255, unique=True)
    site = models.ForeignKey(SiteModel,null=True,blank=True,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name
