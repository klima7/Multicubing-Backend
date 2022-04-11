import os
import threading
import time
import logging
import schedule
from django.apps import AppConfig


class SchedutilConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':

            logging.basicConfig()
            schedule_logger = logging.getLogger('schedule')
            schedule_logger.setLevel(level=logging.DEBUG)

            threading.Thread(target=_schedule_thread, daemon=True).start()


def _schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)
