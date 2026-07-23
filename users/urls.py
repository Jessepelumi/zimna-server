from django.urls import path
from .views import (
    RegisterView,
    PasswordLoginView,
    SendOTPView,
    VerifyOTPView,
    InternalAuthView
)

urlpatterns = [
    # Email & Password
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', PasswordLoginView.as_view(), name='password-login'),

    # Email & OTP
    path('auth/otp/send/', SendOTPView.as_view(), name='otp-send'),
    path('auth/otp/verify/', VerifyOTPView.as_view(), name='otp-verify'),

    # OAuth
    path('auth/internal-auth/', InternalAuthView.as_view(), name='internal-auth'),
]
