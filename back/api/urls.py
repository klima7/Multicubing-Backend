from rest_framework.routers import DefaultRouter
from account.urls import router as account_router

app_name = 'api'

router = DefaultRouter()
router.registry.extend(account_router.registry)

urlpatterns = router.urls
