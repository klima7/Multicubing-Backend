from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account


class AccountAdmin(UserAdmin):
    fieldsets = (
        ('Identity', {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Dates', {'fields': ('date_joined', 'last_seen')}),
    )

    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin', ("last_seen", admin.EmptyFieldListFilter),)
    search_fields = ('username', 'email')
    ordering = ('email',)
    filter_horizontal = tuple()
    add_fieldsets = tuple()


admin.site.register(Account, AccountAdmin)
