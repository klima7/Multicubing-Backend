from django.db import models

from account.models import Account
from room.models import Room


class Participant(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    spectator = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} | {self.room}'
