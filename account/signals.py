import re

from presence.signals import presence_changed
import django
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Account


connected_users_changed = django.dispatch.Signal()


@receiver(presence_changed)
def detect_connected_users_changed(sender, room, added, removed, bulk_change, **kwargs):
    match = re.match(r'^account\.(.*)$', room.channel_name)
    if not match:
        return

    username = match.groups()[0]
    account = Account.objects.filter(username=username).first()
    if account is None:
        return

    new_added = account if added else None
    new_removed = account if removed else None

    connected_users_changed.send(sender=sender, connected=new_added, disconnected=new_removed, bulk_change=bulk_change)


@receiver(post_save, sender=Account)
def on_account_creation_create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(connected_users_changed)
def on_connected_users_changed_update_last_seen(sender, connected, disconnected, bulk_change, **kwargs):
    account = connected if connected else disconnected
    if account:
        account.update_last_seen()
        account.save()
