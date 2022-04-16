from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from cube.models import Cube
from multicubing.signals import SaveDoneSignalMixin


class Room(SaveDoneSignalMixin, models.Model):

    class Meta:
        ordering = ('creation_date',)

    name = models.CharField(max_length=25, unique=True, validators=[MinLengthValidator(3)])
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=25, null=True, blank=True, validators=[MinLengthValidator(3)])
    cube = models.ForeignKey(Cube, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name='Creation date', default=timezone.now, blank=True)

    def __str__(self):
        return self.name

    @property
    def is_private(self):
        return self.password is not None
