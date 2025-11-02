from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "phone", "country", "is_staff")
    list_filter = ("is_staff", "is_superuser", "country")
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("phone", "avatar", "country")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительная информация", {"fields": ("phone", "avatar", "country")}),
    )
