from django.shortcuts import render
from .serializers import LoginSerializer
# Create your views here.
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class LoginAPIView(APIView):
    permission_classes = []  # Allow unauthenticated users to login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)  # Use for validation (optional)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']  # Access authenticated user from serializer (if used)

        # No need to manually log in the user, SimpleJWT handles authentication
        token = RefreshToken.for_user(user)  # Generate a refresh token

        return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)