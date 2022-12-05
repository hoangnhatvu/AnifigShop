from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active')
    list_display_links = ('email', 'username', 'first_name', 'last_name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)