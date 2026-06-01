from django.urls import path

from .views import (
    checklist_add_view,
    checklist_delete_view,
    checklist_toggle_view,
    kanban_update_view,
    tag_list_view,
    tag_delete_view,
    task_create_view,
    task_delete_view,
    task_detail_view,
    task_edit_view,
    task_list_view,
    task_toggle_complete_view,
    task_update_status_view,
)


app_name = "tasks"

urlpatterns = [
    path("tasks/", task_list_view, name="list"),
    path("tasks/create/", task_create_view, name="create"),
    path("tasks/<int:pk>/", task_detail_view, name="detail"),
    path("tasks/<int:pk>/edit/", task_edit_view, name="edit"),
    path("tasks/<int:pk>/delete/", task_delete_view, name="delete"),
    path("tasks/<int:pk>/update-status/", task_update_status_view, name="update_status"),
    path("tasks/<int:pk>/toggle-complete/", task_toggle_complete_view, name="toggle_complete"),
    path("tasks/<int:pk>/checklist/add/", checklist_add_view, name="checklist_add"),
    path("tasks/checklist/<int:pk>/toggle/", checklist_toggle_view, name="checklist_toggle"),
    path("tasks/checklist/<int:pk>/delete/", checklist_delete_view, name="checklist_delete"),
    path("tags/", tag_list_view, name="tags"),
    path("tags/<int:pk>/delete/", tag_delete_view, name="tag_delete"),
    path("kanban/update/", kanban_update_view, name="kanban_update"),
]
