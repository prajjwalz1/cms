from django.shortcuts import render
from cms.mixins import ResponseMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import *
from cms.serializers import *
from django.http import JsonResponse

def BadRequestResponse(request_type, *args, **kwargs):
    print(args)
    return Response({"success": False, "message": f'request {request_type} is not valid'}, status=status.HTTP_400_BAD_REQUEST)


class ContentTypeListView(APIView):
    allowed_models = ["sitemodel", "warehousemodel"]

    def get(self, request):
        content_types = ContentType.objects.filter(model__in=self.allowed_models)
        content_types_data = []

        for ct in content_types:
            model_class = ct.model_class()
            if model_class:
                instances = model_class.objects.all()
                instances_data = [{"id": instance.id, "name": str(instance)} for instance in instances]
                content_types_data.append({
                    "app_label": ct.app_label,
                    "model": ct.model,
                    "id": ct.id,
                    "instances": instances_data
                })
        items=ItemModel.objects.all()
        item_serialzer=ItemModelSerializer(items,many=True)

        return Response({"success": True,"items":item_serialzer.data, "content_types": content_types_data}, status=status.HTTP_200_OK)

class WorkflowRequest(ResponseMixin, APIView):
    pagination_class = PageNumberPagination

    def post(self, request):
        request_type = request.GET.get("request")
        print(request_type)
        
        if request_type == "create_workflow":
            return self.CreateWorkflowRequest(request)
        else:
            return BadRequestResponse(request_type)
        
    def CreateWorkflowRequest(self,request):
        serializer=RequestWorkflowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.handle_success_response(status.HTTP_201_CREATED,serialized_data=serializer.data,message="successfully created workflow")
        else:
             return self.handle_serializererror_response(status.HTTP_400_BAD_REQUEST,**serializer.errors)

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
