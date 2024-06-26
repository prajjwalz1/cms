from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from cms.mixins import ResponseMixin
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
