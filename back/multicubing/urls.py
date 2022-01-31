from django.contrib import admin
from django.urls import path, include
from .apps.index.views import index
from .apps.api import urls as api_urls

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include(api_urls))
]
