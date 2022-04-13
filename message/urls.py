from django.urls import path

from .views import MessagesView

urlpatterns = [
    path('rooms/<room_slug>/messages', MessagesView.as_view()),
]
