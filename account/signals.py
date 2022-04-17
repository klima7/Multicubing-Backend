import re

from presence.signals import presence_changed
import django
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Account


user_connected = django.dispatch.Signal()
user_disconnected = django.dispatch.Signal()


@receiver(presence_changed)
def detect_connected_users_changed(sender, room, added, removed, **kwargs):
    # check if correct room
    match = re.match(r'^account\.(.*)$', room.channel_name)
    if not match:
        return

    # get associated account
    username = match.groups()[0]
    account = Account.objects.filter(username=username).first()
    if account is None:
        return

    # send specific signals
    if added:
        user_connected.send(sender=sender, user=account)
    if removed:
        user_disconnected.send(sender=sender, user=account)


@receiver(user_connected)
def on_user_connected_update_last_seen(sender, user, **kwargs):
    user.update_last_seen()
    user.save()


@receiver(user_disconnected)
def on_user_disconnected_update_last_seen(sender, user, **kwargs):
    user.update_last_seen()
    user.save()


@receiver(post_save, sender=Account)
def on_account_creation_create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
