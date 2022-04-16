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
room_participants_changed = django.dispatch.Signal()
room_participant_joined = django.dispatch.Signal()
room_participant_left = django.dispatch.Signal()
room_participants_bulk_change = django.dispatch.Signal()


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
        added = added.user
    if removed:
        removed = removed.user

    room_participants_changed.send(sender=sender, room=real_room, added=added, removed=removed, bulk_change=bulk_change)
    if added:
        room_participant_joined.send(sender=sender, room=real_room, user=added)
    if removed:
        room_participant_left.send(sender=sender, room=real_room, user=removed)
    if bulk_change:
        room_participants_bulk_change.send(sender=sender)


@receiver(room_participants_changed)
def on_room_participants_changed_send_room_notification(sender, room, added, removed, bulk_change, **kwargs):
    if added or removed:
        send_room_update(room.slug)
    elif bulk_change:
        send_rooms_refresh()


@receiver(save_done, sender=Room)
def on_room_update_send_notification(sender, old, new, **kwargs):
    send_room_update(new.slug)


@receiver(post_delete, sender=Room)
def on_room_delete_send_notification(sender, instance, **kwargs):
    send_room_delete(instance.slug)


def send_room_update(room_slug):
    room = Room.objects.filter(slug=room_slug).first()
    if room is None:
        return
    read_serializer = RoomsReadSerializer(room)
    async_to_sync(get_channel_layer().group_send)('rooms', {'type': 'rooms.created', 'room': read_serializer.data})


def send_room_delete(room_slug):
    async_to_sync(get_channel_layer().group_send)('rooms', {'type': 'rooms.deleted', 'slug': room_slug})


def send_rooms_refresh():
    async_to_sync(get_channel_layer().group_send)('rooms', {'type': 'rooms.refresh'})


@receiver(room_participants_changed)
def on_room_participants_changed_send_users_notifications(sender, room, added, removed, bulk_change, **kwargs):
    channel_name = f'rooms.{room.slug}'
    if added:
        serialized_user = AccountSerializer(added).data
        async_to_sync(get_channel_layer().group_send)(channel_name, {'type': 'users.update', 'user': serialized_user})
    if removed:
        async_to_sync(get_channel_layer().group_send)(channel_name, {'type': 'users.delete', 'username': removed.username})
    if bulk_change:
        async_to_sync(get_channel_layer().group_send)(channel_name, {'type': 'users.refresh'})
