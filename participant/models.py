from django.db import models

from account.models import Account
from room.models import Room


class Participant(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    spectator = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} | {self.room}'

    def notify_update(self):
        from .serializers import ParticipantSerializer
        serialized_user = ParticipantSerializer(self).data
        self.room.send({'type': 'participants.update', 'participant': serialized_user})

    def notify_delete(self):
        self.room.send({'type': 'participants.delete', 'username': self.user.username})
