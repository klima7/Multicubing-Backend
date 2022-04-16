from rest_framework import serializers

from account.serializers import AccountSerializer
from .models import Participant


class ParticipantSerializer(serializers.ModelSerializer):

    user = AccountSerializer()
    room = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Participant
        fields = ['user', 'room', 'spectator']
