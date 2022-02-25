from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomCreateSerializer, RoomReadSerializer
from .models import Room
from cube.models import Cube
from django.utils.text import slugify
from api.utils import ErrorResponse


class RoomViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = RoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        slug = slugify(data['name'])
        exists = Room.objects.filter(slug=slug).exists()
        if exists:
            return ErrorResponse(status=status.HTTP_409_CONFLICT, error='name-taken')
        cube = Cube.objects.get(identifier=data['cube'])
        room = Room(name=data['name'], description=data['description'], slug=slug, password=data['password'], cube=cube)
        room.save()

        read_serializer = RoomReadSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        rooms = Room.objects.all()
        serializer = RoomReadSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
