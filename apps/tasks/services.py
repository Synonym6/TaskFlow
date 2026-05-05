from collections import defaultdict
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import ActivityLog, Task


def log_activity(owner, action, description, task=None, project=None):
    return ActivityLog.objects.create(
        owner=owner,
        task=task,
        project=project,
        action=action,
        description=description,
    )


def build_statistics(user):
    tasks = Task.objects.filter(owner=user)
    completed_by_day = (
        tasks.filter(status=Task.StatusChoices.DONE, completed_at__isnull=False)
        .annotate(day=TruncDate("completed_at"))
        .values("day")
        .annotate(total=Count("id"))
        .order_by("day")
    )

    status_counts = defaultdict(int)
    for item in tasks.values("status").annotate(total=Count("id")):
        status_counts[item["status"]] = item["total"]

    priority_counts = defaultdict(int)
    for item in tasks.values("priority").annotate(total=Count("id")):
        priority_counts[item["priority"]] = item["total"]

    week_start = timezone.now().date() - timedelta(days=6)
    completion_labels = []
    completion_values = []
    day_map = {entry["day"]: entry["total"] for entry in completed_by_day if entry["day"]}
    for offset in range(7):
        date_point = week_start + timedelta(days=offset)
        completion_labels.append(date_point.strftime("%d.%m"))
        completion_values.append(day_map.get(date_point, 0))

    return {
        "completion_labels": completion_labels,
        "completion_values": completion_values,
        "status_counts": status_counts,
        "priority_counts": priority_counts,
        "overdue_count": tasks.filter(deadline__lt=timezone.now()).exclude(status=Task.StatusChoices.DONE).count(),
    }
