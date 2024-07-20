from django.shortcuts import render

# Create your views here.
from cms.mixins import ResponseMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from inventory.models import *
from .serializer import *
from concurrent.futures import ThreadPoolExecutor

class Inventory(APIView):

    def get(self, request, *args, **kwargs):

        def fetch_warehouse_inventory():
            return WareHouseInventory.objects.all()

        def fetch_site_inventory():
            return SiteInventory.objects.all()

        with ThreadPoolExecutor() as executor:
            future_warehouse_inventory = executor.submit(fetch_warehouse_inventory)
            future_site_inventory = executor.submit(fetch_site_inventory)

            warehouse_inventory_qs = future_warehouse_inventory.result()
            site_inventory_qs = future_site_inventory.result()

        serializers = {
            "warehouse_serializer": (warehouseInventorySerialzier, warehouse_inventory_qs),
            "site_serializer": (SiteInventorySerialzier, site_inventory_qs)
        }

        serialized_data = self.serialize_concurrently(serializers)

        return Response({"success":True,"message":"Inventory fetched successfully","data":{"warehouse_stock":serialized_data["warehouse_serializer"],"site_stock":serialized_data["site_serializer"]}},status=status.HTTP_200_OK)

    def serialize_concurrently(self, serializers):
            def serialize(serializer_class, queryset):
                serializer = serializer_class(queryset, many=True)
                data = serializer.data
                return data

            with ThreadPoolExecutor() as executor:
                futures = {
                    name: executor.submit(serialize, serializer_class, queryset)
                    for name, (serializer_class, queryset) in serializers.items()
                }

                results = {name: future.result() for name, future in futures.items()}
            
            return results
    

