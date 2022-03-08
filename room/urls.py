from django.urls import path
from .views import RoomsView, PermitsView
from . import consumers

urlpatterns = [
    path('rooms/', RoomsView.as_view()),
    path('rooms/<room_slug>/permit/', PermitsView.as_view()),
]

ws_urlpatterns = [
    path('', consumers.ChatConsumer.as_asgi()),
    path('<room_slug>/', consumers.RoomConsumer.as_asgi()),
]
