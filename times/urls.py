from django.urls import path

from .views import TimesView, TurnsView

urlpatterns = [
    path('rooms/<room_slug>/times/', TimesView.as_view()),
    path('rooms/<room_slug>/turns/', TurnsView.as_view()),
]
