from django.db import models
from room.models import Room
from account.models import Account


class Permit(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room.name} - {self.account.username}'
