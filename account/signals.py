import re

from channels_presence.signals import presence_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Account


@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(presence_changed)
def update_active(sender, room, added, removed, bulk_change, **kwargs):
    match = re.match('^account.(.*)$', room.channel_name)
    if not match:
        return

    username = match.groups()[0]
    account = Account.objects.filter(username=username).first()
    if account is None:
        return

    account.update_active()
    account.save()
