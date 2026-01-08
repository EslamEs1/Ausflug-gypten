"""
Admin configuration for Users app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = _('User Profile')
    verbose_name_plural = _('User Profile')
    fields = ['phone', 'country', 'city', 'address', 'language_preference', 'newsletter_subscribed', 'avatar']


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'country', 'city', 'language_preference', 'newsletter_subscribed']
    list_filter = ['language_preference', 'newsletter_subscribed', 'country']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

