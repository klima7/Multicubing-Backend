from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import ErrorResponse
from cube.models import Cube
from .models import Room, Permit
from .serializers import RoomCreateSerializer, RoomsReadSerializer, RoomReadSerializer, PermitSerializer


class RoomsView(APIView):

    def post(self, request):
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

        read_serializer = RoomsReadSerializer(room)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomsReadSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomView(APIView):

    def get(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        serializer = RoomReadSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermitsView(APIView):

    def get(self, request, room_slug):
        permit = True
        account = request.user
        room = get_object_or_404(Room, slug=room_slug)
        if room.password is not None:
            permit = Permit.objects.filter(account=account, room__slug=room_slug).first() is not None
        return Response({'permit': permit}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PermitSerializer)
    def post(self, request, room_slug):
        room = get_object_or_404(Room, slug=room_slug)
        serializer = PermitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        if room.password == password:
            existing = Permit.objects.filter(account=request.user, room=room).first()
            if not existing:
                permit = Permit(account=request.user, room=room)
                permit.save()
            return Response({})
        else:
            return ErrorResponse('invalid-password', status=401)
