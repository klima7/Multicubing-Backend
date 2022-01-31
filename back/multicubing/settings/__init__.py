import os

DEFAULT_MULTICUBING_ENVIRONMENT = 'development'


def setup_settings():
    os.environ.setdefault('MULTICUBING_ENVIRONMENT', DEFAULT_MULTICUBING_ENVIRONMENT)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'multicubing.settings.' + os.environ.get('MULTICUBING_ENVIRONMENT')
