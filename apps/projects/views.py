from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from apps.tasks.services import build_statistics, log_activity

from .forms import ProjectForm
from .models import Project


@login_required
def project_list_view(request):
    projects = Project.objects.filter(owner=request.user).annotate(task_count=Count("tasks"))
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        log_activity(request.user, _("Создан проект"), _("Создан проект %(title)s") % {"title": project.title}, project=project)
        messages.success(request, _("Проект создан."))
        return redirect("projects:list")
    return render(request, "projects/project_list.html", {"projects": projects, "form": form})


@login_required
def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    tasks = project.tasks.select_related("project").prefetch_related("tags")
    edit_form = ProjectForm(request.POST or None, instance=project, prefix="edit")
    project_status_summary = [
        {"label": _("К выполнению"), "value": tasks.filter(status="todo").count()},
        {"label": _("В работе"), "value": tasks.filter(status="in_progress").count()},
        {"label": _("Тестирование"), "value": tasks.filter(status="testing").count()},
        {"label": _("Готово"), "value": tasks.filter(status="done").count()},
    ]
    recent_activity = project.activity_logs.select_related("task")[:5]

    if request.method == "POST" and request.POST.get("action") == "update_project" and edit_form.is_valid():
        edit_form.save()
        log_activity(request.user, _("Обновлен проект"), _("Проект %(title)s обновлен") % {"title": project.title}, project=project)
        messages.success(request, _("Проект обновлен."))
        return redirect("projects:detail", pk=project.pk)

    if request.method == "POST" and request.POST.get("action") == "delete_project":
        title = project.title
        project.delete()
        messages.success(request, _("Проект %(title)s удален.") % {"title": title})
        return redirect("projects:list")

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
            "edit_form": edit_form,
            "project_status_summary": project_status_summary,
            "recent_activity": recent_activity,
        },
    )
