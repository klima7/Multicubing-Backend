from rest_framework import serializers


class PermitSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=25)
