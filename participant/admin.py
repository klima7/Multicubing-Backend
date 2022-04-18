from django.contrib import admin

from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'room', 'spectator')


admin.site.register(Participant, ParticipantAdmin)
