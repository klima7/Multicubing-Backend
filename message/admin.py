from django.contrib import admin

from .models import Message


class PermitAdmin(admin.ModelAdmin):
    list_display = ('content', 'sender')


admin.site.register(Message, PermitAdmin)
