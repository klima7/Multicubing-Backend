from django.contrib import admin

from .models import Turn, Time


class TimeAdmin(admin.ModelAdmin):
    list_display = ('time', 'user', 'flag', 'turn')


admin.site.register(Time, TimeAdmin)


class TimeInlineAdmin(admin.TabularInline):
    model = Time
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class TurnAdmin(admin.ModelAdmin):
    list_display = ('number', 'room', 'scramble')
    inlines = [TimeInlineAdmin]


admin.site.register(Turn, TurnAdmin)
