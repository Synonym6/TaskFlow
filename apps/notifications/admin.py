from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Notification


@admin.action(description=_("Отметить выбранные уведомления прочитанными"))
def mark_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.action(description=_("Отметить выбранные уведомления непрочитанными"))
def mark_unread(modeladmin, request, queryset):
    queryset.update(is_read=False)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "type", "is_read", "related_task", "related_project", "created_at")
    list_editable = ("is_read",)
    list_filter = ("type", "is_read", "created_at")
    search_fields = ("title", "message", "owner__username", "owner__email")
    autocomplete_fields = ("owner", "related_task", "related_project")
    list_select_related = ("owner", "related_task", "related_project")
    date_hierarchy = "created_at"
    ordering = ("is_read", "-created_at")
    readonly_fields = ("created_at",)
    actions = (mark_read, mark_unread)
