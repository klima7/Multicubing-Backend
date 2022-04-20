from django.urls import path

from .views import TimesView, TurnsView, TurnView, NestedTimesView

urlpatterns = [
    path('rooms/<room_slug>/times/', TimesView.as_view()),
    path('rooms/<room_slug>/turns/', TurnsView.as_view()),
    path('rooms/<room_slug>/turns/<int:turn_number>/', TurnView.as_view()),
    path('rooms/<room_slug>/turns/<int:turn_number>/times/', NestedTimesView.as_view()),
]
