from django.http.response import Http404, JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

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


def custom_500_exception_handler(request):
    data = {'error': 'server-error'}
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def custom_400_exception_handler(request, exception):
    data = {'error': 'bad-request'}
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)