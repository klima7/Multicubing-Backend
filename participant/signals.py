from django.dispatch import receiver
from django.utils import timezone

from .signals_def import *


@receiver(participant_first_connected)
def on_first_connected_actions(sender, room, participant, **kwargs):
    # make participant active
    participant.active = True
    participant.save()

    # update room last_activity
    room = participant.room
    room.last_activity = None
    room.save()

    # notify
    participant.notify_update()


@receiver(participant_last_disconnected)
def on_last_disconnected_actions(sender, room, participant, **kwargs):
    # make participant inactive
    participant.active = False
    participant.save()

    # update room last_activity
    room = participant.room
    active_count = room.participant_set.filter(active=True).count()
    if active_count == 0:
        room.last_activity = timezone.now()
        room.save()

    # notify
    participant.notify_delete()
