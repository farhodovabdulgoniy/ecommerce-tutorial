from django.contrib import admin
from sympy import im
from .models import Account
from django.contrib.auth.admin import UserAdmin
from datetime import datetime


class AccountAdmin(UserAdmin):
    list_display = ['email','first_name','last_name','username','last_login','date_joined','is_active']
    list_display_links = ['email','username','first_name']
    readonly_fields = ['last_login','date_joined']
    ordering = ['-date_joined']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin)


def delete_user(request):
    user = Account.objects.filter(is_active=False)
    for u in user:

        time = datetime.now()-u.date_joined()

        if user.date_joined - time > 1:
            user.delete()

    return super().delete_user