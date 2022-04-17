from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone

from .models import Account
from .signals_def import *


@receiver(post_save, sender=Account)
def on_account_creation_create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(account_first_connected)
def on_first_connected_make_user_active(sender, user, **kwargs):
    user.last_seen = None
    user.save()


@receiver(account_last_disconnected)
def on_last_disconnected_make_user_inactive(sender, user, **kwargs):
    user.last_seen = timezone.now()
    user.save()
