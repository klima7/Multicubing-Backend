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


class TimePutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = ('time', 'flag')

    def create(self, validated_data):
        return Time.objects.create(
            turn=validated_data['turn'],
            user=validated_data['user'],
            time=validated_data['time'],
            flag=validated_data['flag'],
        )


class TimesViewQueryParams(serializers.Serializer):

    turn = serializers.IntegerField(required=False)
    username = serializers.ListField(child=serializers.CharField(), required=False)
