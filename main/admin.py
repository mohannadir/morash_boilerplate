from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from main.models import User
from unfold.admin import ModelAdmin
from modules.billing.admin import SubscriptionInline

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "user_actions")
    inlines = (SubscriptionInline,)
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Billing"), {"fields": ("stripe_customer_id", "credits_balance")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    def user_actions(self, obj):
        # Impersonate user
        impersonate_button = f'''
            <a class="bg-white text-gray-500 hover:text-gray-700 dark:bg-gray-900 dark:border-gray-700 dark:hover:text-gray-200 dark:text-gray-400 border cursor-pointer font-medium p-3 my-2 rounded-md shadow-sm text-sm" 
            href="{reverse("impersonate-start", args=[obj.pk])}">Impersonate</a>
        '''

        actions = [impersonate_button]
        return format_html(" | ".join(actions))
    
    user_actions.short_description = "Actions"
    user_actions.allow_tags = True
