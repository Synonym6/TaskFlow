from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from .forms import LoginForm, ProfileForm, ProfilePreferencesForm, RegisterForm, SecurityPasswordForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
        messages.success(request, _("Регистрация прошла успешно."))
        return redirect("dashboard:home")
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
        if not form.cleaned_data.get("remember_me"):
            request.session.set_expiry(0)
        messages.success(request, _("Вы вошли в аккаунт."))
        return redirect("dashboard:home")
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, _("Вы вышли из системы."))
    return redirect("landing")


def password_reset_placeholder(request):
    return render(request, "auth/password_reset_placeholder.html")


@login_required
def settings_view(request):
    user_form = ProfileForm(request.POST or None, instance=request.user)
    profile_form = ProfilePreferencesForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    password_form = SecurityPasswordForm(request.user, request.POST or None)

    if request.method == "POST":
        tab = request.POST.get("tab", "profile")
        if tab == "profile" and user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data["email"]
            user.save()
            profile = profile_form.save(commit=False)
            if profile_form.cleaned_data.get("remove_avatar"):
                profile.avatar.delete(save=False)
                profile.avatar = None
            profile.save()
            translation.activate(profile.language)
            request.session[translation.LANGUAGE_SESSION_KEY] = profile.language
            messages.success(request, _("Профиль обновлен."))
            return redirect("accounts:settings")
        if tab == "security" and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _("Пароль изменен."))
            return redirect("accounts:settings")

    return render(
        request,
        "settings/settings.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )


@login_required
@require_POST
def theme_toggle_view(request):
    profile = request.user.profile
    current = request.POST.get("theme")
    if current in {"light", "dark"}:
        profile.theme = current
        profile.save(update_fields=["theme", "updated_at"])
        return JsonResponse({"ok": True, "theme": current})
    return JsonResponse({"ok": False}, status=400)
