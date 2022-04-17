from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete
from django.dispatch import receiver

from account.serializers import AccountSerializer
from multicubing.signals import save_done
from .models import Room
from .serializers import RoomsReadSerializer
from .signals_def import *


@receiver((room_connected, room_disconnected))
def on_connection_send_room_notification(sender, room, user, **kwargs):
    send_room_update(room)


@receiver(room_connected)
def on_room_connected_send_users_notifications(sender, room, user, **kwargs):
    channel_name = f'rooms.{room.slug}'
    serialized_user = AccountSerializer(user).data
    async_to_sync(get_channel_layer().group_send)(channel_name, {'type': 'users.update', 'user': serialized_user})


@receiver(room_disconnected)
def on_room_disconnected_send_users_notifications(sender, room, user, **kwargs):
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
