from rest_framework import serializers, fields
from django.db.models import Q

from .models import Account


MIN_USERNAME_LENGTH = 5


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'username', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, username):
        if len(username) < MIN_USERNAME_LENGTH or '@' in username:
            raise serializers.ValidationError(f"Minimum username length is {MIN_USERNAME_LENGTH}")
        return username


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, data):
        error = serializers.ValidationError("Failed to login with given credentials.")

        login = data['login']
        password = data['password']
        accounts = Account.objects.filter(Q(username=login) | Q(email=login)).all()
        if not accounts:
            raise error

        for account in accounts:
            if account.check_password(password):
                data['account'] = account
                return data

        raise error
