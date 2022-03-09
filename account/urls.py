from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AccountViewSet
from .consumers import AccountConsumer

router = SimpleRouter()
router.register('accounts', AccountViewSet, basename='Account')

ws_urlpatterns = [
    path('', AccountConsumer.as_asgi()),
]
