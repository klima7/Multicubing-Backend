from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import RoomViewSet
from . import consumers

router = SimpleRouter()
router.register('rooms', RoomViewSet, basename='Account')

ws_urlpatterns = [
    path(r'', consumers.ChatConsumer.as_asgi())
]
