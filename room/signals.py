import re

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_presence.signals import presence_changed
from channels_presence.models import Presence
import django
from django.db.models.signals import post_delete
from django.dispatch import receiver

from multicubing.signals import save_done
from .models import Room
from .serializers import RoomsReadSerializer


room_participants_changed = django.dispatch.Signal()


@receiver(presence_changed)
def detect_room_participants_changes(sender, room, added, removed, bulk_change, **kwargs):
    match = re.match(r'^rooms\.(.*)$', room.channel_name)
    if not match:
        return
    room_slug = match.groups()[0]
    real_room = Room.objects.filter(slug=room_slug).first()
    if not real_room:
        return
    if added:
        presence = Presence.objects.filter(channel_name=added).first()
        added = presence.user if presence else None
    if removed:
        presence = Presence.objects.filter(channel_name=removed).first()
        removed = presence.user if presence else None
    room_participants_changed.send(sender=sender, room=real_room, added=added, removed=removed, bulk_change=bulk_change)


@receiver(room_participants_changed)
def on_room_participants_changed(sender, room, added, removed, bulk_change, **kwargs):
    if added or removed:
        send_room_update(room.slug)
    elif bulk_change:
        send_rooms_refres()


@receiver(save_done, sender=Room)
def on_room_update(sender, old, new, **kwargs):
    send_room_update(new.slug)


@receiver(post_delete, sender=Room)
def on_room_delete(sender, instance, **kwargs):
    send_room_delete(instance.slug)


def send_room_update(room_slug):
    room = Room.objects.filter(slug=room_slug).first()
    if room is None:
        return
    read_serializer = RoomsReadSerializer(room)
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.created", "room": read_serializer.data})


def send_room_delete(room_slug):
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.deleted", "slug": room_slug})


def send_rooms_refres():
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.refresh"})
