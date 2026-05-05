from django.urls import path

from .views import login_view, logout_view, password_reset_placeholder, register_view, settings_view, theme_toggle_view


app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("forgot-password/", password_reset_placeholder, name="password_reset_placeholder"),
    path("settings/", settings_view, name="settings"),
    path("settings/theme-toggle/", theme_toggle_view, name="theme_toggle"),
]
