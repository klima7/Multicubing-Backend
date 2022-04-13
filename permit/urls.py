from django.urls import path

from .views import PermitsView

urlpatterns = [
    path('rooms/<room_slug>/permits/', PermitsView.as_view()),
]
