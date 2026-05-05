from django.urls import path

from .views import project_detail_view, project_list_view


app_name = "projects"

urlpatterns = [
    path("projects/", project_list_view, name="list"),
    path("projects/create/", project_list_view, name="create"),
    path("projects/<int:pk>/", project_detail_view, name="detail"),
]
