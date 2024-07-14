from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import LoginAPIView,UsersView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('getallusers', UsersView.as_view(), name='token_refresh')
]