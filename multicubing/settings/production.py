from .base import *
import django_heroku
from django.utils.log import DEFAULT_LOGGING

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    'https://multicubing-backend.herokuapp.com' 
]

# Log everything as in debug mode
DEFAULT_LOGGING['handlers']['console']['filters'] = []

django_heroku.settings(locals(), staticfiles=False)
