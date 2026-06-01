from datetime import timedelta

from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.projects.models import Project
from apps.tasks.models import Task

from .models import Notification


def create_notification(owner, title, message, notification_type, related_task=None, related_project=None):
    try:
        return Notification.objects.create(
            owner=owner,
            title=title,
            message=message,
            type=notification_type,
            related_task=related_task,
            related_project=related_project,
        )
    except IntegrityError:
        return None


def generate_user_notifications(user):
    now = timezone.now()
    soon_threshold = now + timedelta(hours=24)
    tasks = Task.objects.filter(owner=user)

    for task in tasks.filter(deadline__date=now.date()).exclude(status=Task.StatusChoices.DONE):
        create_notification(
            owner=user,
            title=_("Дедлайн сегодня"),
            message=_("Задача \"%(title)s\" требует внимания сегодня.") % {"title": task.title},
            notification_type=Notification.NotificationType.DEADLINE_TODAY,
            related_task=task,
        )

    for task in tasks.filter(deadline__gt=now, deadline__lte=soon_threshold).exclude(status=Task.StatusChoices.DONE):
        create_notification(
            owner=user,
            title=_("Скоро дедлайн"),
            message=_("До дедлайна задачи \"%(title)s\" осталось меньше 24 часов.") % {"title": task.title},
            notification_type=Notification.NotificationType.DEADLINE_SOON,
            related_task=task,
        )

    for task in tasks.filter(deadline__lt=now).exclude(status=Task.StatusChoices.DONE):
        create_notification(
            owner=user,
            title=_("Задача просрочена"),
            message=_("Срок задачи \"%(title)s\" уже истек.") % {"title": task.title},
            notification_type=Notification.NotificationType.OVERDUE,
            related_task=task,
        )

    for project in Project.objects.filter(owner=user, is_archived=False):
        progress = project.progress_percent()
        if progress in {50, 100}:
            create_notification(
                owner=user,
                title=_("Прогресс проекта"),
                message=_("Проект \"%(title)s\" достиг %(progress)s%%.") % {"title": project.title, "progress": progress},
                notification_type=Notification.NotificationType.PROJECT_PROGRESS,
                related_project=project,
            )


def create_task_completed_notification(task):
    create_notification(
        owner=task.owner,
        title=_("Задача выполнена"),
        message=_("Задача \"%(title)s\" успешно завершена.") % {"title": task.title},
        notification_type=Notification.NotificationType.TASK_COMPLETED,
        related_task=task,
    )
