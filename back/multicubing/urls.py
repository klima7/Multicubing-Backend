from django.contrib import admin
from django.urls import path, include
from .apps.index.views import index
from .apps.api import urls as api_urls
from .apps.docs import urls as docs_urls

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('docs/', include(docs_urls)),
]
