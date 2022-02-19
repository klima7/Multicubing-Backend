from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)