from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ActivityLog, ChecklistItem, Comment, SubTask, Tag, Task


@admin.action(description=_("Отметить выбранные задачи выполненными"))
def mark_completed(modeladmin, request, queryset):
    for task in queryset:
        task.status = Task.StatusChoices.DONE
        task.save()


@admin.action(description=_("Вернуть выбранные задачи в статус 'К выполнению'"))
def mark_todo(modeladmin, request, queryset):
    for task in queryset:
        task.status = Task.StatusChoices.TODO
        task.save()


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "project", "status", "priority", "deadline", "completed_at")
    list_filter = ("status", "priority", "project", "deadline")
    search_fields = ("title", "description", "owner__username", "owner__email")
    ordering = ("status", "position", "deadline", "-created_at")
    readonly_fields = ("created_at", "updated_at", "completed_at")
    actions = (mark_completed, mark_todo)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "color", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "owner__username", "owner__email")
    ordering = ("name",)


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ("text", "task", "is_done", "position", "created_at")
    list_filter = ("is_done",)
    search_fields = ("text", "task__title")
    ordering = ("task", "position")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("task__title", "author__username", "text")
    ordering = ("-created_at",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "owner", "status", "deadline", "position")
    list_filter = ("status", "deadline")
    search_fields = ("title", "task__title", "owner__username", "owner__email")
    ordering = ("task", "position", "deadline")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("action", "owner", "task", "project", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("description", "action", "owner__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
