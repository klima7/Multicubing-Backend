from presence.models import Room as PresenceRoom
from django.core.validators import MinLengthValidator
from rest_framework import serializers

from .models import Room
from cube.validators import CubeValidator


class RoomCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25, validators=[MinLengthValidator(3)])
    description = serializers.CharField(max_length=100, allow_null=True)
    password = serializers.CharField(max_length=25, allow_null=True, validators=[MinLengthValidator(3)])
    cube = serializers.CharField(max_length=100, validators=[CubeValidator()])


class RoomsReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('name', 'slug', 'description', 'cube', 'private', 'count', 'creation_date')

    cube = serializers.SlugRelatedField(read_only=True, slug_field='identifier')
    private = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_private(self, room):
        return room.password is not None

    def get_count(self, room):
        room = PresenceRoom.objects.filter(channel_name=f'rooms.{room.slug}').first()
        if room is None:
            return 0
        return len(room.get_users())


class RoomReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('name', 'slug', 'description', 'cube', 'private', 'count', 'creation_date')

    cube = serializers.SlugRelatedField(read_only=True, slug_field='identifier')
    private = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_private(self, room):
        return room.password is not None

    def get_count(self, room):
        room = PresenceRoom.objects.filter(channel_name=f'rooms.{room.slug}').first()
        if room is None:
            return 0
        return len(room.get_users())
