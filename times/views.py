from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Turn, Time
from .serializers import TurnSerializer, TimeSerializer
from room.models import Room
from permit.models import Permit


class TimesView(APIView):

    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        times = Time.objects.filter(turn__room=room).all()
        serializer = TimeSerializer(times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NestedTimesView(APIView):

    def get(self, request, room_slug, turn_number):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        turn = get_object_or_404(Turn, room=room, number=turn_number)
        times = turn.time_set.all()
        serializer = TimeSerializer(times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NestedTimeView(APIView):

    def get(self, request, room_slug, turn_number, username):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        time = get_object_or_404(Time, turn__room=room, turn__number=turn_number, user__username=username)
        serializer = TimeSerializer(time)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TurnsView(APIView):

    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        turns = room.turn_set.all()
        serializer = TurnSerializer(turns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TurnView(APIView):

    def get(self, request, room_slug, turn_number):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        turn = get_object_or_404(Turn, room=room, number=turn_number)
        serializer = TurnSerializer(turn)
        return Response(serializer.data, status=status.HTTP_200_OK)
