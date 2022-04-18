import django
from django.dispatch import receiver

from room.signals import room_connected, room_disconnected, room_first_connected, room_last_disconnected
from .models import Participant


__all__ = [
    'participant_connected',
    'participant_disconnected',
    'participant_first_connected',
    'participant_last_disconnected',
]


participant_connected = django.dispatch.Signal()
participant_disconnected = django.dispatch.Signal()

participant_first_connected = django.dispatch.Signal()
participant_last_disconnected = django.dispatch.Signal()


@receiver(room_connected)
def detect_participant_connected(sender, room, user, **kwargs):
    send_participant_signal(participant_connected, sender, room, user)


@receiver(room_first_connected)
def detect_participant_first_connected(sender, room, user, **kwargs):
    send_participant_signal(participant_first_connected, sender, room, user)


@receiver(room_disconnected)
def detect_participant_disconnected(sender, room, user, **kwargs):
    send_participant_signal(participant_disconnected, sender, room, user)


@receiver(room_last_disconnected)
def detect_participant_first_disconnected(sender, room, user, **kwargs):
    send_participant_signal(participant_last_disconnected, sender, room, user)


def send_participant_signal(signal, sender, room, user):
    participant = Participant.objects.filter(room=room, user=user).first()
    if not participant:
        participant = Participant(user=user, room=room)
        participant.save()
    signal.send(sender=sender, room=room, participant=participant)
