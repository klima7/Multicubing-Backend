from rest_framework import serializers

from .models import Turn, Time


class TurnSerializer(serializers.ModelSerializer):

    room = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Turn
        fields = ('room', 'number', 'scramble')


class TimeSerializer(serializers.ModelSerializer):

    turn = serializers.SerializerMethodField('get_turn')
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Time
        fields = ('turn', 'user', 'time', 'flag')

    def get_turn(self, time):
        return time.turn.number
