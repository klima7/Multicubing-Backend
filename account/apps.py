import schedule
from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        schedule.every(10).seconds.do(_presence_pruning_task)
        # noinspection PyUnresolvedReferences
        from .signals import on_account_creation_create_auth_token, on_connected_users_changed_update_last_seen


def _presence_pruning_task():
    from presence.models import Room
    Room.objects.prune_rooms()
    Room.objects.prune_presences()
