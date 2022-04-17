import re

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from presence.signals import presence_changed
import django
from django.db.models.signals import post_delete
from django.dispatch import receiver

from multicubing.signals import save_done
from account.serializers import AccountSerializer
from .models import Room
from .serializers import RoomsReadSerializer


# room participants signals
room_connected = django.dispatch.Signal()
room_disconnected = django.dispatch.Signal()


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
        room_connected.send(sender=sender, room=real_room, user=added.user)
    if removed:
        room_disconnected.send(sender=sender, room=real_room, user=removed.user)


@receiver((room_connected, room_disconnected))
def on_connection_send_room_notification(sender, room, user, **kwargs):
    send_room_update(room)


@receiver(room_connected)
def on_room_participants_changed_send_users_notifications(sender, room, user, **kwargs):
    channel_name = f'rooms.{room.slug}'
    serialized_user = AccountSerializer(user).data
    async_to_sync(get_channel_layer().group_send)(channel_name, {'type': 'users.update', 'user': serialized_user})


@receiver(room_disconnected)
def on_room_participants_changed_send_users_notifications(sender, room, user, **kwargs):
    channel_name = f'rooms.{room.slug}'
    async_to_sync(get_channel_layer().group_send)(channel_name, {'type': 'users.delete', 'username': user.username})


@receiver(save_done, sender=Room)
def on_room_update_send_notification(sender, old, new, **kwargs):
    send_room_update(new)


@receiver(post_delete, sender=Room)
def on_room_delete_send_notification(sender, instance, **kwargs):
    async_to_sync(get_channel_layer().group_send)('rooms', {'type': 'rooms.deleted', 'slug': instance.slug})


def send_room_update(room):
    read_serializer = RoomsReadSerializer(room)
    async_to_sync(get_channel_layer().group_send)('rooms', {'type': 'rooms.created', 'room': read_serializer.data})
