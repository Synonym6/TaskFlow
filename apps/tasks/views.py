import json
from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.notifications.services import create_task_completed_notification

from .forms import ChecklistItemForm, CommentForm, TagForm, TaskForm
from .models import ChecklistItem, Tag, Task
from .services import log_activity


def _task_queryset(user):
    return Task.objects.filter(owner=user).select_related("project").prefetch_related("tags", "checklist_items", "comments__author")


@login_required
def task_list_view(request):
    tasks = _task_queryset(request.user)
    search = request.GET.get("search", "").strip()
    if search:
        tasks = tasks.filter(title__icontains=search)
    if request.GET.get("status"):
        tasks = tasks.filter(status=request.GET["status"])
    if request.GET.get("priority"):
        tasks = tasks.filter(priority=request.GET["priority"])
    if request.GET.get("project"):
        tasks = tasks.filter(project_id=request.GET["project"])
    if request.GET.get("tag"):
        tasks = tasks.filter(tags__id=request.GET["tag"])
    if request.GET.get("deadline") == "overdue":
        tasks = tasks.filter(deadline__lt=timezone.now()).exclude(status=Task.StatusChoices.DONE)
    sort = request.GET.get("sort")
    if sort == "deadline":
        tasks = tasks.order_by("deadline", "-created_at")
    elif sort == "created":
        tasks = tasks.order_by("-created_at")
    elif sort == "priority":
        tasks = tasks.annotate(
            priority_order=Case(
                When(priority=Task.PriorityChoices.HIGH, then=Value(0)),
                When(priority=Task.PriorityChoices.MEDIUM, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by("priority_order", "deadline")

    form = TaskForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        log_activity(request.user, _("Создана задача"), _("Создана задача %(title)s") % {"title": task.title}, task=task, project=task.project)
        messages.success(request, _("Задача создана."))
        return redirect("tasks:list")

    context = {
        "tasks": tasks.distinct(),
        "form": form,
        "projects": request.user.projects.all(),
        "tags": request.user.tags.all(),
        "status_choices": Task.StatusChoices.choices,
        "priority_choices": Task.PriorityChoices.choices,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def task_create_view(request):
    initial = {}
    deadline_date = request.GET.get("date")
    project_id = request.GET.get("project")
    if deadline_date:
        parsed = parse_date(deadline_date)
        if parsed:
            initial["deadline"] = timezone.make_aware(datetime.combine(parsed, time(hour=12)))
    if project_id and project_id.isdigit():
        project = request.user.projects.filter(pk=project_id).first()
        if project:
            initial["project"] = project
    form = TaskForm(request.POST or None, user=request.user, initial=initial)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        log_activity(request.user, _("Создана задача"), _("Создана задача %(title)s") % {"title": task.title}, task=task, project=task.project)
        messages.success(request, _("Задача создана."))
        return redirect("tasks:detail", pk=task.pk)
    return render(request, "tasks/task_form.html", {"form": form, "page_title": _("Новая задача")})


@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(_task_queryset(request.user), pk=pk)
    checklist_form = ChecklistItemForm(request.POST or None, prefix="checklist")
    comment_form = CommentForm(request.POST or None, prefix="comment")

    if request.method == "POST":
        if request.POST.get("action") == "add_checklist" and checklist_form.is_valid():
            item = checklist_form.save(commit=False)
            item.task = task
            item.position = task.checklist_items.count()
            item.save()
            log_activity(request.user, _("Добавлен чеклист"), item.text, task=task, project=task.project)
            return redirect("tasks:detail", pk=task.pk)
        if request.POST.get("action") == "add_comment" and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            log_activity(request.user, _("Добавлен комментарий"), comment.text, task=task, project=task.project)
            return redirect("tasks:detail", pk=task.pk)
        if request.POST.get("action") == "delete_task":
            title = task.title
            task.delete()
            messages.success(request, _("Задача %(title)s удалена.") % {"title": title})
            return redirect("tasks:list")

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
            "checklist_form": checklist_form,
            "comment_form": comment_form,
        },
    )


@login_required
def task_edit_view(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    form = TaskForm(request.POST or None, instance=task, user=request.user)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        if task.status == Task.StatusChoices.DONE:
            create_task_completed_notification(task)
        log_activity(request.user, _("Обновлена задача"), _("Обновлена задача %(title)s") % {"title": task.title}, task=task, project=task.project)
        messages.success(request, _("Задача обновлена."))
        return redirect("tasks:detail", pk=task.pk)
    return render(request, "tasks/task_form.html", {"form": form, "task": task, "page_title": _("Редактировать задачу")})


@login_required
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, _("Задача %(title)s удалена.") % {"title": title})
        return redirect("tasks:list")
    return render(request, "tasks/task_delete_confirm.html", {"task": task})


@login_required
@require_POST
def task_toggle_complete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.status = Task.StatusChoices.DONE if task.status != Task.StatusChoices.DONE else Task.StatusChoices.TODO
    task.save()
    if task.status == Task.StatusChoices.DONE:
        create_task_completed_notification(task)
    log_activity(request.user, _("Изменен статус"), _("Статус задачи %(title)s изменен") % {"title": task.title}, task=task, project=task.project)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "status": task.status})
    return redirect("tasks:detail", pk=task.pk)


@login_required
@require_POST
def task_update_status_view(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    status = request.POST.get("status")
    if status not in dict(Task.StatusChoices.choices):
        return JsonResponse({"ok": False, "error": _("Недопустимый статус.")}, status=400)
    task.status = status
    task.save()
    if status == Task.StatusChoices.DONE:
        create_task_completed_notification(task)
    log_activity(request.user, _("Обновлен статус"), _("Задача %(title)s перемещена") % {"title": task.title}, task=task, project=task.project)
    return JsonResponse({"ok": True, "status": task.status})


@login_required
@require_POST
def checklist_add_view(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    form = ChecklistItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.task = task
        item.position = task.checklist_items.count()
        item.save()
        log_activity(request.user, _("Добавлен чеклист"), item.text, task=task, project=task.project)
        return JsonResponse({"ok": True, "item_id": item.pk, "text": item.text})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def checklist_toggle_view(request, pk):
    item = get_object_or_404(ChecklistItem.objects.select_related("task"), pk=pk, task__owner=request.user)
    item.is_done = not item.is_done
    item.save(update_fields=["is_done"])
    log_activity(request.user, _("Обновлен чеклист"), item.text, task=item.task, project=item.task.project)
    return JsonResponse({"ok": True, "is_done": item.is_done})


@login_required
def tag_list_view(request):
    tags = Tag.objects.filter(owner=request.user)
    form = TagForm(request.POST or None, user=request.user)
    edit_tag = None
    edit_form = None
    if request.GET.get("edit"):
        edit_tag = get_object_or_404(Tag, pk=request.GET["edit"], owner=request.user)
        edit_form = TagForm(request.POST or None, instance=edit_tag, user=request.user, prefix="edit")
    if request.method == "POST" and request.POST.get("action") != "edit_tag" and form.is_valid():
        form.save()
        messages.success(request, _("Тег создан."))
        return redirect("tasks:tags")
    if request.method == "POST" and request.POST.get("action") == "edit_tag" and edit_form and edit_form.is_valid():
        edit_form.save()
        messages.success(request, _("Тег обновлен."))
        return redirect("tasks:tags")
    return render(request, "tags/tag_list.html", {"tags": tags, "form": form, "edit_form": edit_form, "edit_tag": edit_tag})


@login_required
@require_POST
def tag_delete_view(request, pk):
    tag = get_object_or_404(Tag, pk=pk, owner=request.user)
    tag.delete()
    messages.success(request, _("Тег удален."))
    return redirect("tasks:tags")


@login_required
@require_POST
def checklist_delete_view(request, pk):
    item = get_object_or_404(ChecklistItem.objects.select_related("task"), pk=pk, task__owner=request.user)
    task_pk = item.task.pk
    item.delete()
    messages.success(request, _("Пункт чеклиста удален."))
    return redirect("tasks:detail", pk=task_pk)


@login_required
@require_POST
def kanban_update_view(request):
    payload = json.loads(request.body or "{}")
    task_id = payload.get("task_id")
    status = payload.get("status")
    position = payload.get("position", 0)
    if status not in dict(Task.StatusChoices.choices):
        return JsonResponse({"ok": False, "error": _("Недопустимый статус.")}, status=400)
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    task.status = status
    task.position = max(int(position), 0)
    task.save()
    if task.status == Task.StatusChoices.DONE:
        create_task_completed_notification(task)
    log_activity(request.user, _("Kanban обновлен"), _("Задача %(title)s перемещена") % {"title": task.title}, task=task, project=task.project)
    return JsonResponse({"ok": True})
