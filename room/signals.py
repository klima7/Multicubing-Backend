import re

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_presence.signals import presence_changed
from django.db.models.signals import post_delete
from django.dispatch import receiver

from multicubing.signals import save_done
from .models import Room
from .serializers import RoomsReadSerializer


@receiver(save_done, sender=Room)
def on_room_update(sender, old, new, **kwargs):
    send_room_updated(new.slug)


@receiver(post_delete, sender=Room)
def on_room_delete(sender, instance, **kwargs):
    send_room_deleted(instance.slug)


@receiver(presence_changed)
def on_room_users_change(sender, room, added, removed, bulk_change, **kwargs):
    match = re.match(r'^rooms\.(.*)$', room.channel_name)
    if not match:
        return
    room_slug = match.groups()[0]

    if added or removed:
        send_room_updated(room_slug)
    elif bulk_change:
        send_rooms_refresh()


def send_room_updated(room_slug):
    room = Room.objects.filter(slug=room_slug).first()
    if room is None:
        return
    read_serializer = RoomsReadSerializer(room)
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.created", "room": read_serializer.data})


def send_room_deleted(room_slug):
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.deleted", "slug": room_slug})


def send_rooms_refresh():
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.refresh"})
