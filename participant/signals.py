from django.dispatch import receiver

from .signals_def import *


@receiver(participant_first_connected)
def make_participant_active(sender, room, participant, **kwargs):
    participant.active = True
    participant.save()


@receiver(participant_last_disconnected)
def make_participant_inactive(sender, room, participant, **kwargs):
    participant.active = False
    participant.save()
