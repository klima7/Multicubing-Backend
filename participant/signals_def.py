import django
from django.dispatch import receiver

from room.signals import room_connected
from .models import Participant


__all__ = [
    'room_connected_without_participant',
    'room_connected_with_participant',
]


room_connected_without_participant = django.dispatch.Signal()
room_connected_with_participant = django.dispatch.Signal()


@receiver(room_connected)
def detect_room_connected_without_participant(sender, room, user, **kwargs):
    participant = Participant.objects.filter(room=room, user=user).first()
    if participant is None:
        room_connected_without_participant.send(sender=sender, room=room, user=user)
    else:
        room_connected_with_participant.send(sender=sender, room=room, participant=participant)
