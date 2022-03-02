from rest_framework.routers import DefaultRouter
from account.urls import router as account_router
from django.urls import path, include

app_name = 'api'

router = DefaultRouter()
router.registry.extend(account_router.registry)

urlpatterns = [
    *router.urls,
    path('', include('room.urls')),
]
