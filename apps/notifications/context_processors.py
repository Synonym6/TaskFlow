from .models import Notification


def notification_summary(request):
    if not request.user.is_authenticated:
        return {"unread_notifications_count": 0, "recent_notifications": []}

    qs = Notification.objects.filter(owner=request.user)
    return {
        "unread_notifications_count": qs.filter(is_read=False).count(),
        "recent_notifications": qs[:5],
    }
