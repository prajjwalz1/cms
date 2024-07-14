from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer,UserSerializer
from cms.mixins import ResponseMixin
from .models import CustomUser
from rest_framework.pagination import PageNumberPagination

class LoginAPIView(APIView,ResponseMixin):
    permission_classes = []  # Allow unauthenticated users to login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return self.handle_success_response(
                status.HTTP_200_OK,
                serialized_data={
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        },)


class UsersView(APIView,ResponseMixin):
    pagination_class = PageNumberPagination
    def get(self,request):
        paginator=self.pagination_class()
        obj=CustomUser.objects.all()
        paginated_user_objects=paginator.paginate_queryset(obj,request)
        serializer=UserSerializer(paginated_user_objects,many=True)
        return self.handle_success_response(status.HTTP_200_OK,serialized_data=serializer.data)
        