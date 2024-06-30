from cms.models import *
from cms.serializers import *
from cms.mixins import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


def client_view(request):
    return HttpResponse("CMS Tenants Response")


# ----------------------------- CATEGORY --------------------------------------------
class CategoryAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):

        request_type=request.GET.get("request")
        if request_type and request_type=="getallcategory":
            return self.getallcategory(self)
        

        try:
            paginator = self.pagination_class()
            category = CategoryModel.objects.all()
            paginated_category = paginator.paginate_queryset(category, request)
            serializer = CategoryModelSerializer(paginated_category, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def getallcategory(self,request):
        category = CategoryModel.objects.all()
        serializer=CategoryModelSerializer(category,many=True)
        return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )

    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created Category",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        category, category_error = self.get_object(CategoryModel, pk)
        if not category:
            return self.handle_error_response(category_error, status.HTTP_404_NOT_FOUND)
        serializer = CategoryModelSerializer(category)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        category, category_error = self.get_object(CategoryModel, pk)
        if not category:
            return self.handle_error_response(category_error, status.HTTP_404_NOT_FOUND)
        serializer = CategoryModelSerializer(category, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Category",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category, category_error = self.get_object(CategoryModel, pk)
        if not category:
            return self.handle_error_response(category_error, status.HTTP_404_NOT_FOUND)
        category.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Category",
        )


# ----------------------------- BRAND --------------------------------------------
class BrandAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            brand = BrandModel.objects.all()
            paginated_brand = paginator.paginate_queryset(brand, request)
            serializer = BrandModelSerializer(paginated_brand, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = BrandModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created brand",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class BrandDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        brand, brand_error = self.get_object(BrandModel, pk)
        if not brand:
            return self.handle_error_response(brand_error, status.HTTP_404_NOT_FOUND)
        serializer = BrandModelSerializer(brand)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        brand, brand_error = self.get_object(BrandModel, pk)
        if not brand:
            return self.handle_error_response(brand_error, status.HTTP_404_NOT_FOUND)
        serializer = BrandModelSerializer(brand, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Brand",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        brand, brand_error = self.get_object(BrandModel, pk)
        if not brand:
            return self.handle_error_response(brand_error, status.HTTP_404_NOT_FOUND)
        brand.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Brand",
        )


# ----------------------------- SUPPLIER --------------------------------------------
class SupplierAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            supplier = SupplierModel.objects.all()
            paginated_supplier = paginator.paginate_queryset(supplier, request)
            serializer = SupplierModelSerializer(paginated_supplier, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = SupplierModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created Supplier",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class SupplierDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        supplier, supplier_error = self.get_object(SupplierModel, pk)
        if not supplier:
            return self.handle_error_response(supplier_error, status.HTTP_404_NOT_FOUND)
        serializer = SupplierModelSerializer(supplier)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        supplier, supplier_error = self.get_object(SupplierModel, pk)
        if not supplier:
            return self.handle_error_response(supplier_error, status.HTTP_404_NOT_FOUND)
        serializer = SupplierModelSerializer(supplier, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Supplier",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        supplier, supplier_error = self.get_object(SupplierModel, pk)
        if not supplier:
            return self.handle_error_response(supplier_error, status.HTTP_404_NOT_FOUND)
        supplier.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Supplier",
        )


# ----------------------------- WAREHOUSE --------------------------------------------
class WarehouseAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            warehouse = WarehouseModel.objects.all()
            paginated_warehouse = paginator.paginate_queryset(warehouse, request)
            serializer = WarehouseModelSerializer(paginated_warehouse, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = WarehouseModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created warehouse",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class WarehouseDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        warehouse, warehouse_error = self.get_object(WarehouseModel, pk)
        if not warehouse:
            return self.handle_error_response(
                warehouse_error, status.HTTP_404_NOT_FOUND
            )
        serializer = WarehouseModelSerializer(warehouse)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        warehouse, warehouse_error = self.get_object(WarehouseModel, pk)
        if not warehouse:
            return self.handle_error_response(
                warehouse_error, status.HTTP_404_NOT_FOUND
            )
        serializer = WarehouseModelSerializer(warehouse, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Warehouse",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        warehouse, warehouse_error = self.get_object(WarehouseModel, pk)
        if not warehouse:
            return self.handle_error_response(
                warehouse_error, status.HTTP_404_NOT_FOUND
            )
        warehouse.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Warehouse",
        )


# ----------------------------- PRODUCT --------------------------------------------
class ProductAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            product = ProductModel.objects.all()
            paginated_product = paginator.paginate_queryset(product, request)
            serializer = ProductModel_SelectRelated_Serializer(
                paginated_product, many=True
            )
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ProductModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created Product",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        product, product_error = self.get_object(ProductModel, pk)
        if not product:
            return self.handle_error_response(product_error, status.HTTP_404_NOT_FOUND)
        serializer = ProductModel_SelectRelated_Serializer(product)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        product, product_error = self.get_object(ProductModel, pk)
        if not product:
            return self.handle_error_response(product_error, status.HTTP_404_NOT_FOUND)
        serializer = ProductModelSerializer(product, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Product",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product, product_error = self.get_object(ProductModel, pk)
        if not product:
            return self.handle_error_response(product_error, status.HTTP_404_NOT_FOUND)
        product.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Product",
        )


# ----------------------------- VEHICLE --------------------------------------------
class VehicleAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            vehicle = VehicleModel.objects.all()
            paginated_vehicle = paginator.paginate_queryset(vehicle, request)
            serializer = VehicleModel_SelectRelated_Serializer(
                paginated_vehicle, many=True
            )
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = VehicleModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created Vehicle",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class VehicleDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        vehicle, vehicle_error = self.get_object(VehicleModel, pk)
        if not vehicle:
            return self.handle_error_response(vehicle_error, status.HTTP_404_NOT_FOUND)
        print(vehicle,"vehicle")
        serializer = VehicleModel_SelectRelated_Serializer(vehicle)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        ) 

    def patch(self, request, pk):
        vehicle, vehicle_error = self.get_object(VehicleModel, pk)
        if not vehicle:
            return self.handle_error_response(vehicle_error, status.HTTP_404_NOT_FOUND)
        serializer = VehicleModelSerializer(vehicle, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Vehicle",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vehicle, vehicle_error = self.get_object(VehicleModel, pk)
        if not vehicle:
            return self.handle_error_response(vehicle_error, status.HTTP_404_NOT_FOUND)
        vehicle.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Vehicle",
        )


# ----------------------------- SITE --------------------------------------------
class SiteAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            site = SiteModel.objects.all()
            paginated_site = paginator.paginate_queryset(site, request)
            serializer = SiteModel_SelectRelated_Serializer(paginated_site, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = SiteModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created Site",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class SiteDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        site, site_error = self.get_object(SiteModel, pk)
        if not site:
            return self.handle_error_response(site_error, status.HTTP_404_NOT_FOUND)
        serializer = SiteModel_SelectRelated_Serializer(site)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        site, site_error = self.get_object(SiteModel, pk)
        if not site:
            return self.handle_error_response(site_error, status.HTTP_404_NOT_FOUND)
        serializer = SiteModelSerializer(site, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Site",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        site, site_error = self.get_object(SiteModel, pk)
        if not site:
            return self.handle_error_response(site_error, status.HTTP_404_NOT_FOUND)
        site.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Site",
        )


# ----------------------------- GROUP --------------------------------------------
class GroupAPIView(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            group = GroupModel.objects.all()
            paginated_group = paginator.paginate_queryset(group, request)
            serializer = GroupModel_SelectRelated_Serializer(paginated_group, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = GroupModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created Group",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)


class GroupDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        group, group_error = self.get_object(GroupModel, pk)
        if not group:
            return self.handle_error_response(group_error, status.HTTP_404_NOT_FOUND)
        serializer = GroupModel_SelectRelated_Serializer(group)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        group, group_error = self.get_object(GroupModel, pk)
        if not group:
            return self.handle_error_response(group_error, status.HTTP_404_NOT_FOUND)
        serializer = GroupModelSerializer(group, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Group",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group, group_error = self.get_object(GroupModel, pk)
        if not group:
            return self.handle_error_response(group_error, status.HTTP_404_NOT_FOUND)
        group.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Group",
        )


class ProjectView(APIView,ResponseMixin):
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            qs = Project.objects.all()
            print(qs)
            paginated_group = paginator.paginate_queryset(qs, request)
            print(paginated_group)
            serializer = project_SelectRelated_Serializer(paginated_group, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_201_CREATED,
                serialized_data=serializer.data,
                message="Successfully Created Group",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)
        
class ProjectDetailAPIView(ResponseMixin, GetSingleObjectMixin, APIView):
    def get(self, request, pk):
        project, project_error = self.get_object(Project, pk)
        if not project:
            return self.handle_error_response(project_error, status.HTTP_404_NOT_FOUND)
        serializer = project_SelectRelated_Serializer(project)
        return self.handle_success_response(
            status.HTTP_200_OK,
            serialized_data=serializer.data,
        )

    def patch(self, request, pk):
        project, project_error = self.get_object(Project, pk)
        if not project:
            return self.handle_error_response(project_error, status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data=serializer.data,
                message="Successfully updated Group",
            )
        except ValidationError as e:
            error_detail = e.detail
            error_detail.update({"success": False})
            raise e
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project, project_error = self.get_object(Project, pk)
        if not project:
            return self.handle_error_response(project_error, status.HTTP_404_NOT_FOUND)
        project.delete()
        return self.handle_success_response(
            status.HTTP_204_NO_CONTENT,
            message="Successfully deleted Group",
        )