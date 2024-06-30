from django.shortcuts import render
from cms.mixins import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import *
def BadRequestResponse(*args, **kwargs):
    return Response({"success":False,"message":f'request {kwargs.get("request_type")} is not valid'},status=status.HTTP_400_BAD_REQUEST)


class WorkflowRequest(ResponseMixin,APIView):
    pagination_class=PageNumberPagination
    def post(self,request):
        request_type=request.GET.get("request")
        if request_type=="request_transport":
            return self.TransportRequest(request)
        else:
            return BadRequestResponse({"request_type":request_type})
        
    def MachineryRequest(request):
        request_from=request.data.get("from")
        request_dest=request.data.get("request_dest")
        request_item=request.data.get("request_item")
        from_date=request.data.get("from_date")
        to_date=request.data.get("to_date")
        purpose=request.data.get("purpose")
        purpose=request.data.get("project")

    def VehicleRequest(request):
        request_from=request.data.get("from")
        request_dest=request.data.get("request_dest")
        vehicle=request.data.get("request_item")
        from_date=request.data.get("from_date")
        purpose=request.data.get("purpose")

        pagination_class = PageNumberPagination

    def get(self, request):
        try:
            paginator = self.pagination_class()
            qs = Workflow.objects.all()
            paginated_brand = paginator.paginate_queryset(qs, request)
            serializer = WorkflowSerializer(paginated_brand, many=True)
            return self.handle_success_response(
                status.HTTP_200_OK, serialized_data=serializer.data
            )
        except Exception as e:
            return self.handle_error_response(str(e), status.HTTP_400_BAD_REQUEST)




from django.http import JsonResponse
from .models import SiteModel, WarehouseModel, SupplierModel

def get_objects(request):
    model = request.GET.get('model')
    print(model)
    if model == 'sitemodel':
        objects = SiteModel.objects.all().values('id', 'name')
    elif model == 'warehousemodel':
        print("here")
        objects = WarehouseModel.objects.all().values('id', 'name')
    elif model == 'suppliermodel':
        objects = SupplierModel.objects.all().values('id', 'name')
    else:
        objects = []

    json_data = list(objects)
    print(json_data)
    return JsonResponse(list(objects), safe=False)
