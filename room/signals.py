from multicubing.signals import save_done
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Room
from .serializers import RoomReadSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(save_done, sender=Room)
def notify_room_update(sender, old, new, **kwargs):
    read_serializer = RoomReadSerializer(new)
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.created", "room": read_serializer.data})


@receiver(post_delete, sender=Room)
def notify_room_delete(sender, instance, **kwargs):
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.deleted", "slug": instance.slug})
