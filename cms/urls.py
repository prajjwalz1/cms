from django.contrib import admin
from django.urls import path
from django.conf import settings
from cms.views import *

urlpatterns = [
    # path(settings.ADMIN_PANEL_URL, admin.site.urls),
    path("", client_view),  # Tenant Checkup
    # -------------CATEGORY----------------------------
    path("category/", CategoryAPIView.as_view(), name="category_list"),
    path("getallcategory/", CategoryAPIView.as_view(), name="category_list"),
    path(
        "category/<int:pk>/",
        CategoryDetailAPIView.as_view(),
        name="category_detail",
    ),
    # -------------BRAND----------------------------
    path("brand/", BrandAPIView.as_view(), name="brand_list"),
    path(
        "brand/<int:pk>/",
        BrandDetailAPIView.as_view(),
        name="brand_detail",
    ),
    # -------------SUPPLIER----------------------------
    path("supplier/", SupplierAPIView.as_view(), name="supplier_list"),
    path(
        "supplier/<int:pk>/",
        SupplierDetailAPIView.as_view(),
        name="supplier_detail",
    ),
    # -------------WAREHOUSE----------------------------
    path("warehouse/", WarehouseAPIView.as_view(), name="warehouse_list"),
    path(
        "warehouse/<int:pk>/",
        WarehouseDetailAPIView.as_view(),
        name="warehouse_detail",
    ),
    # -------------PRODUCT----------------------------
    path("product/", ProductAPIView.as_view(), name="product_list"),
    path(
        "product/<int:pk>/",
        ProductDetailAPIView.as_view(),
        name="product_detail",
    ),
    # -------------VEHICLE----------------------------
    path("vehicle/", VehicleAPIView.as_view(), name="vehicle_list"),
    path(
        "vehicle/<int:pk>/",
        VehicleDetailAPIView.as_view(),
        name="vehicle_detail",
    ),
    # -------------SITE----------------------------
    path("site/", SiteAPIView.as_view(), name="site_list"),
    path(
        "site/<int:pk>/",
        SiteDetailAPIView.as_view(),
        name="site_detail",
    ),
    # -------------GROUP----------------------------
    path("group/", GroupAPIView.as_view(), name="group_list"),
    path(
        "group/<int:pk>/",
        GroupDetailAPIView.as_view(),
        name="group_detail",
    ),

     # -------------Project----------------------------
    path("project/", ProjectView.as_view(), name="Project_list"),
    path(
        "project/<int:pk>/",
        GroupDetailAPIView.as_view(),
        name="group_detail",
    ),
    path("bluebook-renew/", vehicle_form, name="vehicle_form"),
]
