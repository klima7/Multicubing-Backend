from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from docs import urls as docs_urls
from api.urls import ws_urlpatterns as api_ws_urlpatterns

handler500 = 'multicubing.exceptions.custom_500_exception_handler'

handler400 = 'multicubing.exceptions.custom_400_exception_handler'

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('auth/', include('rest_framework.urls')),
    path('docs/', include(docs_urls)),
]

ws_urlpatterns = api_ws_urlpatterns
