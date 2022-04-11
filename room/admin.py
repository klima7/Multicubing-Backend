from django.contrib import admin

from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'cube', 'is_private', 'creation_date')
    list_filter = (('password', admin.EmptyFieldListFilter),)


admin.site.register(Room, RoomAdmin)
