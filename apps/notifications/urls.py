from django.urls import path

from .views import mark_all_read_view, notification_list_view


app_name = "notifications"

urlpatterns = [
    path("notifications/", notification_list_view, name="list"),
    path("notifications/mark-all-read/", mark_all_read_view, name="mark_all_read"),
]
