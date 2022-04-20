from rest_framework import serializers

from .models import Time, Turn


class TimeSerializer(serializers.ModelSerializer):

    turn = serializers.SerializerMethodField('get_turn')

    class Meta:
        model = Time
        fields = ('turn', 'user', 'time', 'flag')

    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    def get_turn(self, time):
        return time.turn.number
