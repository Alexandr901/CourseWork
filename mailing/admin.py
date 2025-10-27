from django.contrib import admin

from .models import Client, Mailing, MailingAttempt, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "owner", "created_at")
    list_filter = ("owner", "created_at")
    search_fields = ("email", "full_name")
    readonly_fields = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "owner", "created_at")
    list_filter = ("owner", "created_at")
    search_fields = ("subject", "body")
    readonly_fields = ("created_at",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "owner", "created_at")
    list_filter = ("status", "owner", "created_at")
    filter_horizontal = ("clients",)
    readonly_fields = ("created_at",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("mailing", "client", "attempt_time", "status")
    list_filter = ("status", "attempt_time")
    readonly_fields = ("attempt_time",)
    search_fields = ("mailing__message__subject", "client__email")
