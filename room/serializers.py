from rest_framework import serializers
from django.core.validators import MinLengthValidator
from django.shortcuts import get_object_or_404
from channels_presence.models import Room as PresenceRoom
from .models import Room
from cube.validators import CubeValidator


class RoomCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25, validators=[MinLengthValidator(3)])
    description = serializers.CharField(max_length=100, allow_null=True)
    password = serializers.CharField(max_length=25, allow_null=True, validators=[MinLengthValidator(3)])
    cube = serializers.CharField(max_length=100, validators=[CubeValidator()])


class RoomReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('name', 'slug', 'description', 'cube', 'private', 'count', 'creation_date')

    cube = serializers.SlugRelatedField(read_only=True, slug_field='identifier')
    private = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_private(self, obj):
        return obj.password is not None

    def get_count(self, obj):
        room = get_object_or_404(PresenceRoom, channel_name="rooms")
        return len(room.get_users())


class PermitSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=25)
