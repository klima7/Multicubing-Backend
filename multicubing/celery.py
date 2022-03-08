from celery import Celery
from .settings import setup_settings
from datetime import timedelta

setup_settings()

app = Celery('multicubing')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.CELERYBEAT_SCHEDULE = {
    'prune-presence': {
        'task': 'channels_presence.tasks.prune_presence',
        'schedule': timedelta(seconds=30)
    },
    'prune-rooms': {
        'task': 'channels_presence.tasks.prune_rooms',
        'schedule': timedelta(seconds=600)
    },
}
