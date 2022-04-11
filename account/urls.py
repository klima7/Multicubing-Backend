from django.urls import path
from rest_framework.routers import SimpleRouter

from .consumers import AccountConsumer
from .views import AccountViewSet

router = SimpleRouter()
router.register('accounts', AccountViewSet, basename='Account')

ws_urlpatterns = [
    path('', AccountConsumer.as_asgi()),
]
