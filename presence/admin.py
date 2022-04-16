from django.contrib import admin

from .models import Room, Presence


class PresenceInlineAdmin(admin.TabularInline):
    model = Presence
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class RoomAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'get_users_count')
    inlines = [
        PresenceInlineAdmin,
    ]


class PresenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'last_seen')


admin.site.register(Room, RoomAdmin)
admin.site.register(Presence, PresenceAdmin)
