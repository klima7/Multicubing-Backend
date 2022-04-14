from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete
from django.dispatch import receiver

from multicubing.signals import save_done
from .models import Message
from .serializers import MessageReadSerializer


@receiver(save_done, sender=Message)
def on_message_update_send_notification(sender, old, new, **kwargs):
    send_message_update(new)


@receiver(post_delete, sender=Message)
def on_message_delete_send_notification(sender, instance, **kwargs):
    send_message_delete(instance)


def send_message_update(message):
    read_serializer = MessageReadSerializer(message)
    print(f'rooms.{message.room}', read_serializer.data)
    async_to_sync(get_channel_layer().group_send)(f'rooms.{message.room.slug}', {'type': 'messages.update', 'message': read_serializer.data})


def send_message_delete(message):
    async_to_sync(get_channel_layer().group_send)(f'rooms.{message.room.slug}', {'type': 'messages.delete', 'id': message.id})
