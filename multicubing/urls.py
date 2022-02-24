from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from docs import urls as docs_urls

handler500 = 'rest_framework.exceptions.server_error'

handler400 = 'rest_framework.exceptions.bad_request'

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('auth/', include('rest_framework.urls')),
    path('docs/', include(docs_urls)),
]
