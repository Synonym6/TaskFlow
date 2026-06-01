from django.contrib import admin

from apps.tasks.models import ActivityLog, Task

from .models import Project


class ProjectTaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("title", "owner", "status", "priority", "deadline", "position")
    readonly_fields = ("owner",)
    show_change_link = True
    ordering = ("status", "position", "deadline")

    def has_add_permission(self, request, obj=None):
        return False


class ProjectActivityLogInline(admin.TabularInline):
    model = ActivityLog
    extra = 0
    fields = ("action", "description", "owner", "task", "created_at")
    readonly_fields = ("action", "description", "owner", "task", "created_at")
    can_delete = False
    ordering = ("-created_at",)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "progress_percent", "total_tasks", "deadline", "is_archived", "created_at")
    list_editable = ("is_archived",)
    list_filter = ("is_archived", "deadline", "created_at")
    search_fields = ("title", "description", "owner__username", "owner__email")
    autocomplete_fields = ("owner",)
    list_select_related = ("owner",)
    date_hierarchy = "deadline"
    ordering = ("is_archived", "deadline", "-updated_at")
    readonly_fields = ("created_at", "updated_at", "progress_percent", "total_tasks", "completed_tasks", "overdue_tasks")
    inlines = (ProjectTaskInline, ProjectActivityLogInline)
