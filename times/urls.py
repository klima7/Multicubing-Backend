from django.urls import path

from .views import TimesView

urlpatterns = [
    path('rooms/<room_slug>/times/', TimesView.as_view()),
]
