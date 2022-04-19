from django.db import models


from room.models import Room


class Turn(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.IntegerField()
    scramble = models.TextField(null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'number'], name='unique_room_number'),
        ]

    def __str__(self):
        return f'Turn(room={self.room}; number={self.number})'


class Time(models.Model):

    class Flag(models.TextChoices):
        DNF = 'DNF', 'DNF'
        PLUS2 = '+2', '+2'

    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    time = models.FloatField(null=True, blank=True, default=None)
    flag = models.TextField(choices=Flag.choices, null=True, blank=True, default=None)

    def __str__(self):
        return f'Time({self.time}; turn={self.turn}; flag={self.flag})'
