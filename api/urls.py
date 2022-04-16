from channels.routing import URLRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.urls import router as account_router
from account.urls import ws_urlpatterns as account_ws_urlpatterns
from room.urls import ws_urlpatterns as room_ws_urlpatterns

app_name = 'api'

router = DefaultRouter()
router.registry.extend(account_router.registry)

urlpatterns = [
    *router.urls,
    path('', include('room.urls')),
    path('', include('permit.urls')),
    path('', include('message.urls')),
    path('', include('participant.urls')),
]

ws_urlpatterns = [
    path('rooms/', URLRouter(room_ws_urlpatterns)),
    path('account/', URLRouter(account_ws_urlpatterns)),
]
