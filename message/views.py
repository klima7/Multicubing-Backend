from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import ErrorResponse


class MessagesView(APIView):

    def get(self, request, room_slug):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, room_slug):
        return Response({}, status=status.HTTP_200_OK)
