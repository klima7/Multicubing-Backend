from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from account.models import Account
from room.models import Room
from multicubing.signals import SaveDoneSignalMixin


class Message(SaveDoneSignalMixin, models.Model):

    class Meta:
        ordering = ('send_time',)

    content = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    send_time = models.DateTimeField(default=timezone.now, blank=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        msg = self.content[:20]
        if len(self.content) > 20:
            msg += '...'
        return msg

    @property
    def is_private(self):
        return self.description is not None
