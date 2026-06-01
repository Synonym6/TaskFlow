import json
from calendar import IllegalMonthError, monthcalendar, monthrange
from datetime import timedelta

from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.formats import date_format
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.notifications.services import generate_user_notifications
from apps.projects.models import Project
from apps.tasks.models import ActivityLog, Task
from apps.tasks.services import build_statistics


def landing_page(request):
    return render(request, "landing.html")


def _time_greeting():
    hour = timezone.localtime().hour
    if hour < 12:
        return _("Доброе утро")
    if hour < 18:
        return _("Добрый день")
    return _("Добрый вечер")


def _month_delta(queryset, current_filter, previous_filter):
    current = queryset.filter(**current_filter).count()
    previous = queryset.filter(**previous_filter).count()
    if previous == 0:
        if current == 0:
            return None
        return {"direction": "up", "value": None, "label": _("Новые данные в этом месяце")}
    delta = round(((current - previous) / previous) * 100)
    return {
        "direction": "up" if delta >= 0 else "down",
        "value": abs(delta),
        "label": _("%(value)s%% с прошлого месяца") % {"value": abs(delta)},
    }


def _weekly_progress(tasks):
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    labels = [str(_("Пн")), str(_("Вт")), str(_("Ср")), str(_("Чт")), str(_("Пт")), str(_("Сб")), str(_("Вс"))]
    values = []
    for offset in range(7):
        day = week_start + timedelta(days=offset)
        day_tasks = tasks.filter(deadline__date=day)
        total = day_tasks.count()
        completed = day_tasks.filter(status=Task.StatusChoices.DONE).count()
        values.append(round((completed / total) * 100) if total else 0)
    return {"labels": labels, "values": values}


def _calendar_context(tasks):
    today = timezone.localdate()
    year = today.year
    month = today.month
    task_dates = {}
    overdue_dates = set()
    for task in tasks.exclude(deadline__isnull=True):
        local_date = timezone.localtime(task.deadline).date()
        if local_date.year == year and local_date.month == month:
            task_dates.setdefault(local_date.day, 0)
            task_dates[local_date.day] += 1
            if task.is_overdue:
                overdue_dates.add(local_date.day)

    weeks = []
    for week in monthcalendar(year, month):
        row = []
        for day in week:
            row.append(
                {
                    "day": day,
                    "is_current_month": day != 0,
                    "is_today": day == today.day,
                    "has_tasks": day in task_dates,
                    "task_count": task_dates.get(day, 0),
                    "is_overdue": day in overdue_dates,
                }
            )
        weeks.append(row)
    return {
        "month_label": date_format(today, "F Y"),
        "weekdays": [_("Пн"), _("Вт"), _("Ср"), _("Чт"), _("Пт"), _("Сб"), _("Вс")],
        "weeks": weeks,
    }


@login_required
def dashboard_home_view(request):
    generate_user_notifications(request.user)
    tasks = Task.objects.filter(owner=request.user).select_related("project").prefetch_related("tags")
    now = timezone.now()
    local_now = timezone.localtime(now)
    start_of_month = local_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    previous_month_end = start_of_month - timedelta(seconds=1)
    previous_month_start = previous_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    nearest_tasks = tasks.exclude(status=Task.StatusChoices.DONE).exclude(deadline__isnull=True).order_by("deadline")[:5]
    recent_tasks = tasks.order_by("-updated_at", "-created_at")[:7]
    active_projects = Project.objects.filter(owner=request.user, is_archived=False).annotate(
        total_tasks_count=Count("tasks"),
        completed_tasks_count=Count("tasks", filter=Q(tasks__status=Task.StatusChoices.DONE)),
    )[:4]
    activity_items = ActivityLog.objects.filter(owner=request.user).select_related("task", "project")[:4]
    chart = _weekly_progress(tasks)
    completed_total = tasks.filter(status=Task.StatusChoices.DONE).count()
    total_tasks = tasks.count()
    progress_percent = round((completed_total / total_tasks) * 100) if total_tasks else 0

    total_delta = _month_delta(
        tasks,
        {"created_at__gte": start_of_month},
        {"created_at__gte": previous_month_start, "created_at__lt": start_of_month},
    )
    in_progress_delta = _month_delta(
        tasks,
        {"updated_at__gte": start_of_month, "status": Task.StatusChoices.IN_PROGRESS},
        {"updated_at__gte": previous_month_start, "updated_at__lt": start_of_month, "status": Task.StatusChoices.IN_PROGRESS},
    )
    completed_delta = _month_delta(
        tasks,
        {"completed_at__gte": start_of_month, "status": Task.StatusChoices.DONE},
        {"completed_at__gte": previous_month_start, "completed_at__lt": start_of_month, "status": Task.StatusChoices.DONE},
    )
    overdue_delta = _month_delta(
        tasks.exclude(status=Task.StatusChoices.DONE),
        {"deadline__gte": start_of_month, "deadline__lt": now},
        {"deadline__gte": previous_month_start, "deadline__lt": start_of_month},
    )

    stat_cards = [
        {
            "label": _("Всего задач"),
            "value": total_tasks,
            "delta": total_delta,
            "icon": "total",
            "tone": "primary",
        },
        {
            "label": _("В работе"),
            "value": tasks.filter(status=Task.StatusChoices.IN_PROGRESS).count(),
            "delta": in_progress_delta,
            "icon": "briefcase",
            "tone": "info",
        },
        {
            "label": _("Выполнено"),
            "value": completed_total,
            "delta": completed_delta,
            "icon": "check",
            "tone": "success",
        },
        {
            "label": _("Просрочено"),
            "value": tasks.filter(deadline__lt=now).exclude(status=Task.StatusChoices.DONE).count(),
            "delta": overdue_delta,
            "icon": "alert",
            "tone": "danger",
        },
    ]

    context = {
        "greeting": _time_greeting(),
        "dashboard_subtitle": _("Вот что происходит с вашими задачами сегодня."),
        "stat_cards": stat_cards,
        "nearest_tasks": nearest_tasks,
        "recent_tasks": recent_tasks,
        "active_projects": active_projects,
        "activity_items": activity_items,
        "calendar_data": _calendar_context(tasks),
        "dashboard_progress_percent": progress_percent,
        "dashboard_chart_empty": total_tasks == 0 or not any(chart["values"]),
        "chart_data": json.dumps(
            {
                "labels": chart["labels"],
                "values": chart["values"],
                "progress": progress_percent,
            }
        ),
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
def kanban_view(request):
    tasks = Task.objects.filter(owner=request.user).select_related("project").prefetch_related("tags").order_by("position", "deadline")
    grouped = {
        "todo": tasks.filter(status=Task.StatusChoices.TODO),
        "in_progress": tasks.filter(status=Task.StatusChoices.IN_PROGRESS),
        "testing": tasks.filter(status=Task.StatusChoices.TESTING),
        "done": tasks.filter(status=Task.StatusChoices.DONE),
    }
    return render(request, "kanban/kanban.html", {"grouped_tasks": grouped})


@login_required
def calendar_view(request):
    today = timezone.localdate()
    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        first_weekday, days_in_month = monthrange(year, month)
    except (TypeError, ValueError, IllegalMonthError):
        year = today.year
        month = today.month
        first_weekday, days_in_month = monthrange(year, month)
    tasks = Task.objects.filter(owner=request.user, deadline__year=year, deadline__month=month).order_by("deadline")
    events = [
        {
            "id": task.pk,
            "title": task.title,
            "date": timezone.localtime(task.deadline).strftime("%Y-%m-%d"),
            "status": task.status,
            "url": reverse("tasks:detail", kwargs={"pk": task.pk}),
        }
        for task in tasks
        if task.deadline
    ]
    return render(
        request,
        "calendar/calendar.html",
        {
            "calendar_year": year,
            "calendar_month": month,
            "days_in_month": range(1, days_in_month + 1),
            "first_weekday": first_weekday,
            "events_json": json.dumps(events),
            "task_create_url": reverse("tasks:create"),
            "today": today,
        },
    )


@login_required
def statistics_view(request):
    tasks = Task.objects.filter(owner=request.user)
    projects = Project.objects.filter(owner=request.user)
    stats = build_statistics(request.user)
    project_progress = [{"title": project.title, "progress": project.progress_percent()} for project in projects]
    has_data = tasks.exists() or projects.exists()
    return render(
        request,
        "statistics/statistics.html",
        {
            "has_data": has_data,
            "stats_json": json.dumps(
                {
                    "completion": {
                        "labels": stats["completion_labels"],
                        "values": stats["completion_values"],
                    },
                    "status": stats["status_counts"],
                    "priority": stats["priority_counts"],
                    "projects": project_progress,
                    "overdue": stats["overdue_count"],
                }
            ),
            "total_tasks": tasks.count(),
            "completed_tasks": tasks.filter(status=Task.StatusChoices.DONE).count(),
            "in_progress_tasks": tasks.filter(status=Task.StatusChoices.IN_PROGRESS).count(),
            "overdue_tasks": stats["overdue_count"],
        },
    )


def handler404_view(request, exception):
    return render(request, "errors/404.html", status=404)


def handler500_view(request):
    return render(request, "errors/500.html", status=500)
