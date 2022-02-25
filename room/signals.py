from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Room
from .serializers import RoomReadSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(pre_save, sender=Room)
def room_pre_save(sender, instance=None, created=False, **kwargs):
    print('sender', sender)
    print('instance', instance)
    print('created', created)
    print('kwargs', kwargs)
    old = Room.objects.filter(pk=instance.pk).first()
    print('old', old)
    if old is None:
        print('Sending')
        read_serializer = RoomReadSerializer(instance)
        async_to_sync(get_channel_layer().group_send)("rooms", {"type": "rooms.created", "room": read_serializer.data})
