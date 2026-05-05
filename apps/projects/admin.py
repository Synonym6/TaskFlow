from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "deadline", "is_archived", "created_at")
    list_filter = ("is_archived", "deadline", "created_at")
    search_fields = ("title", "description", "owner__username", "owner__email")
    ordering = ("is_archived", "deadline", "-updated_at")
