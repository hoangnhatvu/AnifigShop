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

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super(AccountAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

admin.site.register(Account, AccountAdmin)