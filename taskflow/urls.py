from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from apps.dashboard.views import handler404_view, handler500_view, landing_page


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("ru/admin/", RedirectView.as_view(pattern_name="admin:index", permanent=False)),
    path("en/admin/", RedirectView.as_view(pattern_name="admin:index", permanent=False)),
]

urlpatterns += i18n_patterns(
    path("", landing_page, name="landing"),
    path("", include("apps.accounts.urls")),
    path("", include("apps.dashboard.urls")),
    path("", include("apps.tasks.urls")),
    path("", include("apps.projects.urls")),
    path("", include("apps.notifications.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.dashboard.views.handler404_view"
handler500 = "apps.dashboard.views.handler500_view"
