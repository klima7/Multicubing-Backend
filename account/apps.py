import schedule
from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        schedule.every(10).seconds.do(_presence_pruning_task)
        # noinspection PyUnresolvedReferences
        from . import signals


def _presence_pruning_task():
    from presence.models import Room as PresenceRoom
    PresenceRoom.objects.prune_rooms()
    PresenceRoom.objects.prune_presences()

    from room.models import Room
    Room.objects.prune_inactive()
