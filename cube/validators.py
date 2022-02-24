from .models import Cube
from django.core.exceptions import ValidationError


class CubeValidator:

    def __call__(self, value, message='Invalid cube identifier'):
        exists = Cube.objects.filter(identifier=value).exists()
        if not exists:
            raise ValidationError(message, code='notfound', params={'value': value})
