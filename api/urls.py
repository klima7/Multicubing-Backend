from rest_framework.routers import DefaultRouter
from account.urls import router as account_router
from room.urls import router as room_router

app_name = 'api'

router = DefaultRouter()
router.registry.extend(account_router.registry)
router.registry.extend(room_router.registry)

urlpatterns = router.urls
