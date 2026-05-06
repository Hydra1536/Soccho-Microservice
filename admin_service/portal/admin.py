from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import UserProxy


@admin.register(UserProxy)
class UserProxyAdmin(UserAdmin):
    list_display = ["username", "friend_count", "loyalty_score", "encrypted_fields"]
    list_filter = ["is_active"]
    readonly_fields = ["friend_count", "loyalty_score", "encrypted_fields"]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Soccho Stats",
            {
                "fields": ("friend_count", "loyalty_score", "encrypted_fields"),
                "classes": ("collapse",),
            },
        ),
    )

    def encrypted_fields(self, obj):
        return format_html('<span style="color:red">[ENCRYPTED]</span>')

    encrypted_fields.short_description = "Financial Data"
