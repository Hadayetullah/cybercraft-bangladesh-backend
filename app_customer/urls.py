from django.urls import path
from .views import CustomerMessage

urlpatterns = [
    path('message/', CustomerMessage.as_view(), name='customer-message'),
]
