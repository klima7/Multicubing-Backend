from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg import openapi

from .models import Account
from .serializers import AccountSerializer, RegisterSerializer, LoginSerializer
from multicubing.permissions import AuthenticatedExceptActions


@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    manual_parameters=[openapi.Parameter('id', openapi.IN_PATH, description="primary key or 'current'", type=openapi.TYPE_STRING)]
))
class AccountViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [AuthenticatedExceptActions('register', 'login')]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        pk = self.kwargs.get('pk')
        if pk == "current":
            pk = self.request.user.pk
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    @swagger_auto_schema(request_body=RegisterSerializer, responses={201: None}, security=[])
    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        account = Account.objects.create_user(data['email'], data['username'], data['password'])
        data = {
            'response': 'successfully registered a new user.',
            'email': account.email,
            'username': account.username
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=LoginSerializer, responses={201: None}, security=[])
    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        token, created = Token.objects.get_or_create(user=account)
        return Response({'token': token.key})
