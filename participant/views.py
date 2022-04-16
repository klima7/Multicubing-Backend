from rest_framework.response import Response
from rest_framework.views import APIView


class ParticipantsView(APIView):

    def get(self, request, room_slug):
        return Response({})


class ParticipantView(APIView):

    def get(self, request, room_slug, username):
        return Response({})
