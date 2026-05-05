from django.urls import path

from .views import calendar_view, dashboard_home_view, kanban_view, statistics_view


app_name = "dashboard"

urlpatterns = [
    path("dashboard/", dashboard_home_view, name="home"),
    path("kanban/", kanban_view, name="kanban"),
    path("calendar/", calendar_view, name="calendar"),
    path("statistics/", statistics_view, name="statistics"),
]
