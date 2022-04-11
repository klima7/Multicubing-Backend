import os
from django.apps import AppConfig
from .tasks import schedule_tasks


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        from .signals import create_auth_token, update_active
        if os.environ.get('RUN_MAIN', None) != 'true':
            schedule_tasks()
