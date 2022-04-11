from django.urls import path

from .views import PermitsView

urlpatterns = [
    path('permits/<room_slug>/', PermitsView.as_view()),
]
