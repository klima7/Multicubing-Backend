from multicubing.signals import save_done
from django.dispatch import receiver
from .models import Room
from .serializers import RoomReadSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(save_done, sender=Room)
def notify_room_update(sender, old, new, **kwargs):
    read_serializer = RoomReadSerializer(new)
    async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.created", "room": read_serializer.data})
