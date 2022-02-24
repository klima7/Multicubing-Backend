from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from docs import urls as docs_urls
from room import consumers

handler500 = 'rest_framework.exceptions.server_error'

handler400 = 'rest_framework.exceptions.bad_request'

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('auth/', include('rest_framework.urls')),
    path('docs/', include(docs_urls)),
]

websocket_urlpatterns = [
    path(r'ws/rooms/<room_name>/', consumers.ChatConsumer.as_asgi())
]
