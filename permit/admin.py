from django.contrib import admin

from .models import Permit


class PermitAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'room', 'account')


admin.site.register(Permit, PermitAdmin)
