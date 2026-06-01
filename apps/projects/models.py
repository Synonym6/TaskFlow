from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name=_("Владелец"),
    )
    title = models.CharField(max_length=180, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    color = models.CharField(max_length=20, default="#6f61ff", verbose_name=_("Цвет"))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_("Дедлайн"))
    is_archived = models.BooleanField(default=False, verbose_name=_("В архиве"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлен"))

    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекты")
        ordering = ("is_archived", "deadline", "-updated_at")

    def __str__(self):
        return self.title

    def total_tasks(self):
        return self.tasks.count()

    def completed_tasks(self):
        return self.tasks.filter(status="done").count()

    def progress_percent(self):
        total = self.total_tasks()
        return int((self.completed_tasks() / total) * 100) if total else 0

    def overdue_tasks(self):
        return self.tasks.filter(deadline__lt=timezone.now()).exclude(status="done").count()
