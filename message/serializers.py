from rest_framework import serializers
from .models import Message


class MessagePostSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Message.objects.create(
            content=validated_data['content'],
            sender=validated_data['user'],
            room=validated_data['room'],
        )


class MessageReadSerializer(serializers.ModelSerializer):

    room = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    sender = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Message
        fields = ['sender', 'room', 'room', 'send_time', 'content']
