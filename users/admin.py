from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "is_staff",
                    "is_superuser",
                    "password",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
    )
    list_display = ("email", "phone_number", "is_superuser")


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserConfirmation)
