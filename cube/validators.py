from django.core.exceptions import ValidationError

from .models import Cube


class CubeValidator:

    def __call__(self, value, message='Invalid cube identifier'):
        exists = Cube.objects.filter(identifier=value).exists()
        if not exists:
            raise ValidationError(message, code='notfound', params={'value': value})
