from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import ErrorResponse
from .models import Room, Permit
from .serializers import PermitSerializer


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
