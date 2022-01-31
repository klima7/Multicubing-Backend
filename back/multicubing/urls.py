from django.contrib import admin
from django.urls import path, include
from index.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include('api.urls'))
]
