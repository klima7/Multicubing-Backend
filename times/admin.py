from django.contrib import admin

from .models import Turn, Time


class TurnAdmin(admin.ModelAdmin):
    list_display = ('number', 'room', 'scramble')


admin.site.register(Turn, TurnAdmin)


class TimeAdmin(admin.ModelAdmin):
    list_display = ('time', 'user', 'flag', 'turn')


admin.site.register(Time, TimeAdmin)
