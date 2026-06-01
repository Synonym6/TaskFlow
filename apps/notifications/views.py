from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(owner=request.user)
    unread_count = notifications.filter(is_read=False).count()
    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
        },
    )


@login_required
@require_POST
def mark_all_read_view(request):
    Notification.objects.filter(owner=request.user, is_read=False).update(is_read=True)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": True})
