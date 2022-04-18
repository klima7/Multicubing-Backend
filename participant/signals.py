from django.dispatch import receiver

from .models import Participant
from .signals_def import *


@receiver(room_connected_without_participant)
def create_participant_when_needed(sender, room, user, **kwargs):
    participant = Participant(user=user, room=room)
    participant.save()
