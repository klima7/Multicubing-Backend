from django.db import models
from cube.models import Cube
from django.utils import timezone


class Room(models.Model):

    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    password = models.CharField(max_length=25, null=True)
    cube = models.ForeignKey(Cube, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name='date joined', default=timezone.now)

    def __str__(self):
        return self.name
