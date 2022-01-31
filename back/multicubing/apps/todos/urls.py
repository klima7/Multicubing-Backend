from rest_framework.routers import SimpleRouter
from .views import TodoViewSet

router = SimpleRouter()
router.register('todos', TodoViewSet, basename='Todo')
