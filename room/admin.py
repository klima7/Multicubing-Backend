from django.contrib import admin
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Room, RoomAdmin)
