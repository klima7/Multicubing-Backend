from django.db import models

from room.models import Room
from account.models import Account


class Turn(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.IntegerField()
    scramble = models.TextField(null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'number'], name='unique_room_number'),
        ]

    def __str__(self):
        return f'{self.room} | {self.number}'

    def notify_update(self):
        from .serializers import TurnSerializer
        serializer = TurnSerializer(self)
        self.room.send({'type': 'turns.update', 'turn': serializer.data})


class Time(models.Model):

    class Flag(models.TextChoices):
        DNF = 'DNF', 'DNF'
        PLUS2 = '+2', '+2'

    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    time = models.FloatField(null=True, blank=True, default=None)
    flag = models.TextField(choices=Flag.choices, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.time} | {self.user} | {self.turn}'

    def notify_update(self):
        from .serializers import TimeSerializer
        serializer = TimeSerializer(self)
        self.turn.room.send({'type': 'times.update', 'time': serializer.data})
