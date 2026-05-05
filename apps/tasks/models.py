from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name=_("Владелец"),
    )
    name = models.CharField(max_length=80, verbose_name=_("Название"))
    color = models.CharField(max_length=20, default="#6f61ff", verbose_name=_("Цвет"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")
        constraints = [
            models.UniqueConstraint(fields=("owner", "name"), name="unique_tag_per_owner"),
        ]
        ordering = ("name",)

    def __str__(self):
        return self.name


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        TODO = "todo", _("К выполнению")
        IN_PROGRESS = "in_progress", _("В работе")
        TESTING = "testing", _("Тестирование")
        DONE = "done", _("Готово")

    class PriorityChoices(models.TextChoices):
        LOW = "low", _("Низкий")
        MEDIUM = "medium", _("Средний")
        HIGH = "high", _("Высокий")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("Владелец"),
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        related_name="tasks",
        blank=True,
        null=True,
        verbose_name=_("Проект"),
    )
    title = models.CharField(max_length=180, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.TODO,
        verbose_name=_("Статус"),
    )
    priority = models.CharField(
        max_length=20,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
        verbose_name=_("Приоритет"),
    )
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_("Дедлайн"))
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Выполнена"))
    position = models.PositiveIntegerField(default=0, verbose_name=_("Позиция"))
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks", verbose_name=_("Теги"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создана"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлена"))

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")
        ordering = ("status", "position", "deadline", "-created_at")

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return bool(self.deadline and self.deadline < timezone.now() and self.status != self.StatusChoices.DONE)

    def clean(self):
        if not self.title:
            raise ValidationError({"title": _("Название задачи обязательно.")})
        if self.project and self.project.owner_id != self.owner_id:
            raise ValidationError({"project": _("Нельзя привязать задачу к чужому проекту.")})
        if self.deadline and not self.pk and self.deadline < timezone.now() and self.status != self.StatusChoices.DONE:
            raise ValidationError({"deadline": _("Нельзя создать задачу с дедлайном в прошлом.")})

    def save(self, *args, **kwargs):
        if self.status == self.StatusChoices.DONE and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != self.StatusChoices.DONE:
            self.completed_at = None
        self.full_clean()
        super().save(*args, **kwargs)


class ChecklistItem(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="checklist_items",
        verbose_name=_("Задача"),
    )
    text = models.CharField(max_length=255, verbose_name=_("Текст"))
    is_done = models.BooleanField(default=False, verbose_name=_("Выполнен"))
    position = models.PositiveIntegerField(default=0, verbose_name=_("Позиция"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))

    class Meta:
        verbose_name = _("Чеклист")
        verbose_name_plural = _("Чеклисты")
        ordering = ("position", "created_at")

    def __str__(self):
        return self.text


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Задача"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_comments",
        verbose_name=_("Автор"),
    )
    text = models.TextField(verbose_name=_("Комментарий"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлен"))

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.author} -> {self.task}"


class SubTask(models.Model):
    class StatusChoices(models.TextChoices):
        TODO = "todo", _("Не начато")
        IN_PROGRESS = "in_progress", _("В работе")
        DONE = "done", _("Выполнено")

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name=_("Задача"),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name=_("Владелец"),
    )
    title = models.CharField(max_length=180, verbose_name=_("Название"))
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.TODO,
        verbose_name=_("Статус"),
    )
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_("Дедлайн"))
    position = models.PositiveIntegerField(default=0, verbose_name=_("Позиция"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создана"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлена"))

    class Meta:
        verbose_name = _("Подзадача")
        verbose_name_plural = _("Подзадачи")
        ordering = ("position", "created_at")

    def __str__(self):
        return self.title


class ActivityLog(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_logs",
        verbose_name=_("Пользователь"),
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="activity_logs",
        blank=True,
        null=True,
        verbose_name=_("Задача"),
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="activity_logs",
        blank=True,
        null=True,
        verbose_name=_("Проект"),
    )
    action = models.CharField(max_length=120, verbose_name=_("Действие"))
    description = models.TextField(verbose_name=_("Описание"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))

    class Meta:
        verbose_name = _("Запись активности")
        verbose_name_plural = _("Журнал активности")
        ordering = ("-created_at",)

    def __str__(self):
        return self.action
