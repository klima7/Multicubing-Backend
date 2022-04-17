from django.http.response import Http404, JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated, AuthenticationFailed
from rest_framework.views import exception_handler

from api.utils import ErrorResponse


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        return ErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            error='invalid-data',
            details=exc.args[0]
        )
    elif isinstance(exc, NotAuthenticated):
        return ErrorResponse(
            status=status.HTTP_401_UNAUTHORIZED,
            error='not-authenticated',
        )
    elif isinstance(exc, AuthenticationFailed):
        return ErrorResponse(
            status=status.HTTP_401_UNAUTHORIZED,
            error='authentication-failure',
        )
    elif isinstance(exc, PermissionDenied):
        return ErrorResponse(
            status=status.HTTP_403_FORBIDDEN,
            error='permission-denied',
        )
    elif isinstance(exc, Http404):
        return ErrorResponse(
            status=status.HTTP_404_NOT_FOUND,
            error='not-found',
        )
    return None


def custom_500_exception_handler(request):
    return ErrorResponse(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error='server-error',
    )


def custom_400_exception_handler(request, exception):
    return ErrorResponse(
        status=status.HTTP_400_BAD_REQUEST,
        error='bad-request',
    )
