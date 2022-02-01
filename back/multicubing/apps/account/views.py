from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from .models import Account
from .serializers import AccountSerializer, RegistrationSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    @swagger_auto_schema(request_body=RegistrationSerializer, responses={201: None})
    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered a new user.'
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)
