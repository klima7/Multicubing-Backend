from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from permit.models import Permit
from room.models import Room
from .models import Message
from .serializers import MessagePostSerializer, MessageReadSerializer


class MessagesView(APIView):

    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        messages = Message.objects.filter(room=room).all()
        serializer = MessageReadSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        serializer = MessagePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(room=room, user=request.user)

        return Response({}, status=status.HTTP_201_CREATED)
