from rest_framework.routers import SimpleRouter
from .views import AccountViewSet

router = SimpleRouter()
router.register('accounts', AccountViewSet, basename='Account')
