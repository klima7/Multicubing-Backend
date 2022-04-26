from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from drf_yasg.utils import swagger_auto_schema

from .models import Turn, Time
from .serializers import TurnSerializer, TimeSerializer, TimesViewQueryParams, TimePutSerializer
from room.models import Room
from permit.models import Permit
from account.models import Account


class TimesView(APIView):

    @swagger_auto_schema(tags=['times'], query_serializer=TimesViewQueryParams)
    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        times = Time.objects.filter(turn__room=room)
        filtered_times = self.filter(times).all()
        serializer = TimeSerializer(filtered_times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter(self, times):
        filters = self.get_filters()
        if filters['turn'] is not None:
            times = times.filter(turn__number=filters['turn'])
        if filters['usernames'] is not None:
            times = times.filter(user__username__in=filters['usernames'])
        return times

    def get_filters(self):
        params = {key: value[0] for key, value in dict(self.request.query_params).items()}
        filters = {
            'turn': None,
            'usernames': None,
        }

        if 'turn' in params:
            try:
                filters['turn'] = int(params['turn'])
            except:
                raise ValidationError()
        if 'username' in params:
            filters['usernames'] = params['username'].split(',')

        return filters


class NestedTimeView(APIView):

    @swagger_auto_schema(tags=['times'])
    def get(self, request, room_slug, turn_number, username):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        time = get_object_or_404(Time, turn__room=room, turn__number=turn_number, user__username=username)
        serializer = TimeSerializer(time)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['times'], request_body=TimePutSerializer)
    def put(self, request, room_slug, turn_number, username):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        if request.user.username != username:
            raise PermissionDenied('No permission to add time as requested user')

        serializer = TimePutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        turn = get_object_or_404(Turn, number=turn_number)
        time = serializer.save(user=request.user, turn=turn)

        serializer = TimeSerializer(time)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TurnsView(APIView):

    @swagger_auto_schema(tags=['turns'])
    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        turns = room.turn_set.all()
        serializer = TurnSerializer(turns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TurnView(APIView):

    @swagger_auto_schema(tags=['turns'])
    def get(self, request, room_slug, turn_number):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        turn = get_object_or_404(Turn, room=room, number=turn_number)
        serializer = TurnSerializer(turn)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LastTurnView(APIView):

    @swagger_auto_schema(tags=['turns'])
    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        turn = Turn.objects.filter(room=room).order_by('-number').first()
        if turn is None:
            raise NotFound()
        serializer = TurnSerializer(turn)
        return Response(serializer.data, status=status.HTTP_200_OK)
