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
from .permissions import CanApproveWorkflow
def BadRequestResponse(request_type, *args, **kwargs):
    print(args)
    return Response({"success": False, "message": f'request {request_type} is not valid'}, status=status.HTTP_400_BAD_REQUEST)


class ContentTypeListView(APIView):
    allowed_models = ["sitemodel", "warehousemodel","suppliermodel"]

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
        
        if request_type == "materials_request_workflow":
            return self.CreateWorkflowRequest(request)
        if request_type == "CreateFuelRequest":
            return self.CreateFuelRequest(request)
        else:
            return BadRequestResponse(request_type)
        
    def CreateWorkflowRequest(self,request):
        data=request.data.copy()
        data["request_by"]=request.user.id
        serializer=RequestWorkflowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return self.handle_success_response(status.HTTP_201_CREATED,serialized_data=serializer.data,message="successfully created workflow")
        else:
             return self.handle_serializererror_response(status.HTTP_400_BAD_REQUEST,**serializer.errors)
        
    def CreateFuelRequest(self,request):
        payload = request.POST.copy()
        print(payload)
        payload["request_by"]=request.user.id
        serializer=RequestFuelSerializer(data=payload)
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
            serializer = WorkflowSerializer(paginated_brand, many=True,context={'request': request})
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

from io import BytesIO
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from .models import FuelWorkflow
import os

from django.shortcuts import get_object_or_404

def generate_fuel_workflow_report(request, fuel_workflow_id):
    # Query specific FuelWorkflow instance
    fuel_workflow = get_object_or_404(FuelWorkflow, id=fuel_workflow_id)

    # Get template path
    template_path = os.path.join(settings.BASE_DIR, 'workflow/templates/fuelslip.html')

    # Load template
    template = get_template(template_path)

    # Context data for rendering template
    context = {
        'fuel_workflow': fuel_workflow  # Pass the FuelWorkflow instance to the template
    }

    # Render template with context data
    html = template.render(context)

    # Create a BytesIO stream to hold the PDF data
    pdf_file = BytesIO()

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    # Check if PDF generation was successful
    if not pisa_status.err:
        pdf_file.seek(0)  # Reset file pointer to beginning
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="fuel_workflow_report_{fuel_workflow_id}.pdf"'
        pdf_file.close()
        return response
    else:
        pdf_file.close()
        return HttpResponse('Failed to generate PDF', status=400)
    

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
from django.core.files.uploadedfile import UploadedFile

class ApproveWorkflow(APIView,ResponseMixin,GetSingleObjectMixin):
    permission_classes = [CanApproveWorkflow]
    def post(self,request):
        request_type=request.data.get("request_type")
        if request_type=="approve_workflow":
            serializer = ApproveWorkflowSerializer(data=request.data,context={'request': request})
            if serializer.is_valid():
                return self.ApproveMaterialsFlow(request, serializer.validated_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.handle_error_response(error_message="request type is not valid",status_code=400)
    def ApproveMaterialsFlow(self,request,validated_data):
        workflow_id = validated_data.get("workflow_id")
        bill_amount = validated_data.get("bill_amount")
        bill_image = validated_data.get("bill_image")
        
        # Retrieve the workflow object
        workflow, error = self.get_object(Workflow, workflow_id)
        if not workflow:
            return self.handle_error_response(error, status.HTTP_404_NOT_FOUND)
        
        # Update the workflow with new information
        workflow.status = 'approved'
        if bill_amount is not None:
            workflow.bill_amount = bill_amount
        if bill_image and isinstance(bill_image, UploadedFile):
            workflow.bill_image = bill_image
        workflow.save()
        

        return self.handle_success_response(message="workflow approved successfully",status_code=200)
        # Prepare the response data
        response_data = {
            "workflow_id": workflow_id,
            "bill_image": request.build_absolute_uri(workflow.bill_image.url) if workflow.bill_image else None,
            "bill_amount": workflow.bill_amount,
            "message": "Workflow approved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)