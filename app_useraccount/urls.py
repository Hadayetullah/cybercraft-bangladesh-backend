from django.urls import path

from .views import RegisterView, OTPVerifyView, LoginView, LogoutView, RefreshAccessTokenUnauthUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='api_verify_otp'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('refresh-token/', RefreshAccessTokenUnauthUser.as_view(), name='api_token_refresh'),
]