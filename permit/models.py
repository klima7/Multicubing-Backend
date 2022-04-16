from django.db import models
from room.models import Room
from account.models import Account
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed


class PermitManager(models.Manager):

    def check_permission(self, account, room, raise_exception=False):
        if not room.is_private:
            return True
        if account is None:
            raise AuthenticationFailed()
        permit = self.filter(room=room, account=account).first()
        if raise_exception and permit is None:
            raise PermissionDenied()
        return permit is not None


class Permit(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    objects = PermitManager()

    def __str__(self):
        return f'{self.room.name} - {self.account.username}'
