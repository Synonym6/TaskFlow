from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Profile


User = get_user_model()
admin.site.site_header = "TaskFlow Admin"
admin.site.site_title = "TaskFlow Admin"
admin.site.index_title = _("Управление TaskFlow")

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "language", "theme", "notifications_enabled", "created_at")
    list_filter = ("language", "theme", "notifications_enabled")
    search_fields = ("user__username", "user__email", "user__first_name")
    autocomplete_fields = ("user",)
    list_select_related = ("user",)
    ordering = ("-created_at",)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "is_staff", "is_superuser", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    list_select_related = ("profile",)
    date_hierarchy = "date_joined"
    ordering = ("-date_joined",)
    search_fields = ("username", "email", "first_name", "last_name")

    def has_delete_permission(self, request, obj=None):
        if obj and request.user == obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser and "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def delete_model(self, request, obj):
        if request.user == obj and obj.is_superuser:
            raise ValidationError(_("Нельзя удалить собственный superuser аккаунт."))
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        if request.user.is_superuser and queryset.filter(pk=request.user.pk).exists():
            raise ValidationError(_("Нельзя удалить собственный superuser аккаунт."))
        super().delete_queryset(request, queryset)

    def save_model(self, request, obj, form, change):
        if change and request.user.pk == obj.pk and request.user.is_superuser:
            original = User.objects.get(pk=obj.pk)
            if original.is_superuser and not obj.is_superuser:
                raise ValidationError(_("Нельзя снять с себя права superuser."))
            if original.is_staff and not obj.is_staff:
                raise ValidationError(_("Нельзя снять с себя права staff."))
            if original.is_active and not obj.is_active:
                raise ValidationError(_("Нельзя заблокировать себя."))
        super().save_model(request, obj, form, change)
