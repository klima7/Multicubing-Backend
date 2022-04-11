import schedule
from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        schedule.every(10).seconds.do(_presence_pruning_task)
        # noinspection PyUnresolvedReferences
        from .signals import create_auth_token, update_active


def _presence_pruning_task():
    from channels_presence.tasks import prune_presence, prune_rooms
    prune_presence()
    prune_rooms()
