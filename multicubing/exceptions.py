from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework import status
from api.utils import ErrorResponse


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        return ErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            error='invalid-data',
            details=exc.args[0]
        )

    return exception_handler(exc, context)
