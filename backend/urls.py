
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('app_useraccount.urls')),
    path('api/customer/', include('app_customer.urls')),
]
