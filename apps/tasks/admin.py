from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ActivityLog, ChecklistItem, Comment, Tag, Task


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 0
    fields = ("text", "is_done", "position")
    ordering = ("position", "created_at")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("author", "text", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("author",)
    ordering = ("-created_at",)


class ActivityLogInline(admin.TabularInline):
    model = ActivityLog
    extra = 0
    fields = ("action", "description", "owner", "created_at")
    readonly_fields = ("action", "description", "owner", "created_at")
    can_delete = False
    ordering = ("-created_at",)

    def has_add_permission(self, request, obj=None):
        return False


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
    list_display_links = ("title",)
    list_editable = ("status", "priority")
    list_filter = ("status", "priority", "project", "deadline")
    search_fields = ("title", "description", "owner__username", "owner__email")
    autocomplete_fields = ("owner", "project", "tags")
    list_select_related = ("owner", "project")
    date_hierarchy = "deadline"
    ordering = ("status", "position", "deadline", "-created_at")
    readonly_fields = ("created_at", "updated_at", "completed_at")
    actions = (mark_completed, mark_todo)
    inlines = (ChecklistItemInline, CommentInline, ActivityLogInline)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "color", "created_at")
    list_filter = ("created_at", "owner")
    search_fields = ("name", "owner__username", "owner__email")
    autocomplete_fields = ("owner",)
    list_select_related = ("owner",)
    ordering = ("name",)


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ("text", "task", "is_done", "position", "created_at")
    list_filter = ("is_done",)
    search_fields = ("text", "task__title")
    autocomplete_fields = ("task",)
    list_select_related = ("task",)
    ordering = ("task", "position")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("task__title", "author__username", "text")
    autocomplete_fields = ("task", "author")
    list_select_related = ("task", "author")
    ordering = ("-created_at",)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("action", "owner", "task", "project", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("description", "action", "owner__username")
    autocomplete_fields = ("owner", "task", "project")
    list_select_related = ("owner", "task", "project")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
