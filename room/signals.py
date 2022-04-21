from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Room
from .signals_def import *


@receiver((room_connected, room_disconnected))
def on_connection_send_room_notification(sender, room, user, **kwargs):
    room.notify_update()


@receiver(post_delete, sender=Room)
def on_room_delete_send_notification(sender, instance, **kwargs):
    instance.notify_delete()
