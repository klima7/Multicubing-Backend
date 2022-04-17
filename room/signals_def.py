import re

import django
from django.dispatch import receiver

from presence.signals import presence_changed
from presence.models import Presence
from .models import Room


__all__ = [
    'room_connected',
    'room_disconnected',
    'room_first_connected',
    'room_last_disconnected'
]


room_connected = django.dispatch.Signal()
room_disconnected = django.dispatch.Signal()

room_first_connected = django.dispatch.Signal()
room_last_disconnected = django.dispatch.Signal()


@receiver(presence_changed)
def detect_room_connections(sender, room, added, removed, **kwargs):
    # check if proper room
    match = re.match(r'^rooms\.(.*)$', room.channel_name)
    if not match:
        return

    # get room
    room_slug = match.groups()[0]
    real_room = Room.objects.filter(slug=room_slug).first()
    if not real_room:
        return

    # send specific signal
    if added:
        presences_count = Presence.objects.filter(user=added.user, room=room).count()
        if presences_count == 1:
            room_first_connected.send(sender=sender, room=real_room, user=added.user)
        room_connected.send(sender=sender, room=real_room, user=added.user)
    if removed:
        presences_count = Presence.objects.filter(user=removed.user, room=room).count()
        if presences_count == 0:
            room_last_disconnected.send(sender=sender, room=real_room, user=removed.user)
        room_disconnected.send(sender=sender, room=real_room, user=removed.user)
