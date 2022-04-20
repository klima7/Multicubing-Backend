from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from permit.models import Permit
from room.models import Room
from .serializers import ParticipantSerializer, ParticipantSerializerPatch
from .models import Participant


class ParticipantsView(APIView):

    @swagger_auto_schema(tags=['participants'])
    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        participants = Participant.objects.filter(room=room, active=True).all()
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParticipantView(APIView):

    @swagger_auto_schema(tags=['participants'])
    def get(self, request, room_slug, username):
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        participant = get_object_or_404(Participant, active=True, room=room, user__username=username)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['participants'])
    def patch(self, request, room_slug, username):
        # check permission
        room = get_object_or_404(Room, slug=room_slug)
        Permit.objects.check_permission(request.user, room, raise_exception=True)

        # get participant
        participant = get_object_or_404(Participant, active=True, room=room, user__username=username)

        # parse request data
        serializer_patch = ParticipantSerializerPatch(data=request.data)
        serializer_patch.is_valid(raise_exception=True)
        vd = serializer_patch.validated_data

        # perform updates
        if vd['spectator'] is not None:
            participant.spectator = vd['spectator']
        participant.save()

        # return new participant
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_200_OK)
