from rest_framework.routers import DefaultRouter
from ..todos.urls import router as todos_router
from ..account.urls import router as account_router

app_name = 'api'

router = DefaultRouter()
router.registry.extend(todos_router.registry)
router.registry.extend(account_router.registry)

urlpatterns = router.urls
