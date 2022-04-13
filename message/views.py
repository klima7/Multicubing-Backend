from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import ErrorResponse
from permit.models import Permit
from .models import Room
from .serializers import MessagePostSerializer


class MessagesView(APIView):

    def get(self, request, room_slug):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, throw=True)

        # serializer = PermitSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # password = serializer.validated_data['password']
        # if room.password == password:
        #     existing = Permit.objects.filter(account=request.user, room=room).first()
        #     if not existing:
        #         permit = Permit(account=request.user, room=room)
        #         permit.save()
        #     return Response({})
        # else:
        #     return ErrorResponse('invalid-password', status=401)

        return Response({}, status=status.HTTP_200_OK)
