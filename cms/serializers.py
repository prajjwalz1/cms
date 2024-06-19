from rest_framework import serializers
from cms.models import *
from django.contrib.auth.models import User
from django.conf import settings
from users.models import CustomUser
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = "__all__"


class SupplierModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModel
        fields = "__all__"


class WarehouseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseModel
        fields = "__all__"


# ------------------- PRODUCT-------------------------
class ProductModelSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all())

    class Meta:
        model = ProductModel
        fields = "__all__"


class ProductModel_SelectRelated_Serializer(serializers.ModelSerializer):
    category = CategoryModelSerializer()

    class Meta:
        model = ProductModel
        fields = "__all__"


# ------------------- VEHICLE -------------------------
class VehicleModelSerializer(serializers.ModelSerializer):
    contact_person = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = VehicleModel
        fields = "__all__"


class VehicleModel_SelectRelated_Serializer(serializers.ModelSerializer):
    contact_person = UserModelSerializer()

    class Meta:
        model = VehicleModel
        fields = "__all__"


# ------------------- SITE -------------------------
class SiteModelSerializer(serializers.ModelSerializer):
    contact_person = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = SiteModel
        fields = "__all__"


class SiteModel_SelectRelated_Serializer(serializers.ModelSerializer):
    contact_person = UserModelSerializer()

    class Meta:
        model = SiteModel
        fields = "__all__"


# ------------------- GROUP -------------------------
class GroupModelSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=SiteModel.objects.all())

    class Meta:
        model = GroupModel
        fields = "__all__"


class GroupModel_SelectRelated_Serializer(serializers.ModelSerializer):
    site = SiteModelSerializer()

    class Meta:
        model = GroupModel
        fields = "__all__"
