import os

import django_heroku
from django.utils.log import DEFAULT_LOGGING

from .base import *

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    'https://multicubing.herokuapp.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://multicubing-backend.herokuapp.com',
]

CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [os.environ.get('REDIS_URL')]

# Log everything as in debug mode
DEFAULT_LOGGING['handlers']['console']['filters'] = []

django_heroku.settings(locals(), staticfiles=False)
