from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        DEADLINE_TODAY = "deadline_today", _("Дедлайн сегодня")
        DEADLINE_SOON = "deadline_soon", _("Скоро дедлайн")
        OVERDUE = "overdue", _("Просрочено")
        PROJECT_PROGRESS = "project_progress", _("Прогресс проекта")
        TASK_COMPLETED = "task_completed", _("Задача выполнена")
        SYSTEM = "system", _("Системное")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Пользователь"),
    )
    title = models.CharField(max_length=180, verbose_name=_("Заголовок"))
    message = models.TextField(verbose_name=_("Сообщение"))
    type = models.CharField(max_length=30, choices=NotificationType.choices, verbose_name=_("Тип"))
    related_task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notifications",
        verbose_name=_("Связанная задача"),
    )
    related_project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notifications",
        verbose_name=_("Связанный проект"),
    )
    is_read = models.BooleanField(default=False, verbose_name=_("Прочитано"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))

    class Meta:
        verbose_name = _("Уведомление")
        verbose_name_plural = _("Уведомления")
        ordering = ("is_read", "-created_at")
        constraints = [
            models.UniqueConstraint(
                fields=("owner", "type", "related_task"),
                condition=models.Q(related_task__isnull=False),
                name="unique_task_notification_per_type",
            ),
            models.UniqueConstraint(
                fields=("owner", "type", "related_project"),
                condition=models.Q(related_project__isnull=False),
                name="unique_project_notification_per_type",
            ),
        ]

    def __str__(self):
        return self.title
