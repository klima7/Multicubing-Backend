from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from django.http.response import Http404
from rest_framework import status
from api.utils import ErrorResponse


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        return ErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            error='invalid-data',
            details=exc.args[0]
        )
    if isinstance(exc, Http404):
        return ErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            error='not-found',
        )
    return exception_handler(exc, context)


def custom_404_exception_handler(exc, context):
    return ErrorResponse(
        status=status.HTTP_400_BAD_REQUEST,
        error='not-found',
    )
