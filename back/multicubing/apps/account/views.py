from rest_framework import viewsets
from .serializers import AccountSerializer
from .models import Account


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
