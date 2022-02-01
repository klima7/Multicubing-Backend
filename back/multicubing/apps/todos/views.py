from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
