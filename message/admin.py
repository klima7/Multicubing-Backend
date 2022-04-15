from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'sender', 'send_time')


admin.site.register(Message, MessageAdmin)
