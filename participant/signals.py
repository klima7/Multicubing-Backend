from .signals_def import *
from django.dispatch import receiver


@receiver(room_connected_without_participant)
def a(sender, room, user, **kwargs):
    print(f'Connected without participant! {user}; {room}')