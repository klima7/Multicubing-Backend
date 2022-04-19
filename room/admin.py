from django.contrib import admin

from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'cube', 'is_active', 'is_private', 'creation_date')
    list_filter = (('password', admin.EmptyFieldListFilter),)

    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True

    def is_private(self, obj):
        return obj.is_private
    is_private.boolean = True


admin.site.register(Room, RoomAdmin)
