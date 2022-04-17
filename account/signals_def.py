import re

import django
from django.dispatch import receiver

from presence.signals import presence_changed
from presence.models import Presence
from .models import Account


__all__ = [
    'account_connected',
    'account_disconnected',
    'account_first_connected',
    'account_last_disconnected'
]


account_connected = django.dispatch.Signal()
account_disconnected = django.dispatch.Signal()

account_first_connected = django.dispatch.Signal()
account_last_disconnected = django.dispatch.Signal()


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
        presences_count = Presence.objects.filter(user=account, room=room).count()
        if presences_count == 1:
            account_first_connected.send(sender=sender, user=account)
        account_connected.send(sender=sender, user=account)
    if removed:
        presences_count = Presence.objects.filter(user=account, room=room).count()
        if presences_count == 0:
            account_last_disconnected.send(sender=sender, user=account)
        account_disconnected.send(sender=sender, user=account)
