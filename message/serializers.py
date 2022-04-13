from rest_framework import serializers


class MessagePostSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200)
