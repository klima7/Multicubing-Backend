from django.urls import path

from .views import ParticipantsView, ParticipantView

urlpatterns = [
    path('rooms/<room_slug>/participants/', ParticipantsView.as_view()),
    path('rooms/<room_slug>/participants/<username>/', ParticipantView.as_view()),
]
