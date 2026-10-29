from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('boxes/', BoxModelViewSet.as_view(), name='box-list'),
    path('boxes-single/', BoxSingleView.as_view(), name='box-detail'),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('google-auth/', GoogleAuthView.as_view(), name='google_auth'),
    
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('reset-password/', PasswordResetRequestView.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('contact/', ContactView.as_view(), name='contact'),
]
