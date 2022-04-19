from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from .signals_def import *
from .models import Participant
from .serializers import ParticipantSerializer


@receiver(participant_first_connected)
def make_participant_active(sender, room, participant, **kwargs):
    participant.active = True
    participant.save()

    room = participant.room
    room.last_activity = None
    room.save()


@receiver(participant_last_disconnected)
def make_participant_inactive(sender, room, participant, **kwargs):
    participant.active = False
    participant.save()

    room = participant.room
    active_count = room.participant_set.filter(active=True).count()
    if active_count == 0:
        room.last_activity = timezone.now()
        room.save()


@receiver(participant_first_connected)
def send_update_notify(sender, room, participant, **kwargs):
    serialized_user = ParticipantSerializer(participant).data
    room.send({'type': 'participants.update', 'participant': serialized_user})


@receiver(participant_last_disconnected)
def send_delete_notify(sender, room, participant, **kwargs):
    room.send({'type': 'participants.delete', 'username': participant.user.username})


@receiver(post_save, sender=Participant)
def send_participant_update(sender, instance=None, created=False, **kwargs):
    participant = instance
    if participant.active:
        serialized_user = ParticipantSerializer(participant).data
        participant.room.send({'type': 'participants.update', 'participant': serialized_user})
