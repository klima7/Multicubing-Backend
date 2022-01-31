from rest_framework.routers import DefaultRouter
from ..todos.urls import router as todos_router

router = DefaultRouter()
router.registry.extend(todos_router.registry)

urlpatterns = router.urls
