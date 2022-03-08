from multicubing.signals import save_done
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Room
from .serializers import RoomReadSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels_presence.signals import presence_changed


@receiver(save_done, sender=Room)
def notify_room_update(sender, old, new, **kwargs):
    send_room_updated(new.slug)


@receiver(post_delete, sender=Room)
def notify_room_delete(sender, instance, **kwargs):
    send_room_deleted(instance.slug)


@receiver(presence_changed)
def broadcast_presence(sender, room, added, removed, bulk_change, **kwargs):
    room_slug = room.channel_name.rsplit(sep='.', maxsplit=1)[-1]
    if added:
        send_room_updated(room_slug)
    elif removed:
        send_room_deleted(room_slug)
    elif bulk_change:
        send_rooms_refresh()


def send_room_updated(room_slug):
    room = Room.objects.filter(slug=room_slug).first()
    if room is None:
        return
    read_serializer = RoomReadSerializer(room)
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.created", "room": read_serializer.data})


def send_room_deleted(room_slug):
    room = Room.objects.filter(slug=room_slug).first()
    if room is None:
        return
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.deleted", "slug": room.slug})


def send_rooms_refresh():
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.refresh"})
