from rest_framework.routers import DefaultRouter
from ..todos.urls import router as todos_router
from ..account.urls import router as account_router

router = DefaultRouter()
router.registry.extend(todos_router.registry)
router.registry.extend(account_router.registry)

app_name = 'api'

urlpatterns = router.urls
