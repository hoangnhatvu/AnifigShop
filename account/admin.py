from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_active')
    list_display_links = ('email', 'username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name','last_name')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)