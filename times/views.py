from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Time
from .serializers import TimeSerializer
from room.models import Room
from permit.models import Permit


class TimesView(APIView):

    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        times = Time.objects.filter(turn__room=room).all()
        serializer = TimeSerializer(times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
