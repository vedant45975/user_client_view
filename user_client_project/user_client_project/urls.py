from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # <-- Add this line
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]