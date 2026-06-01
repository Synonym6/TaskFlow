from .models import Profile


def language_switch_urls(request):
    query_string = request.META.get("QUERY_STRING", "")
    suffix = f"?{query_string}" if query_string else ""
    path = request.path_info or "/"

    if path == "/en":
        path = "/en/"

    if path.startswith("/en/"):
        ru_path = path[3:] or "/"
        en_path = path
    else:
        ru_path = path
        en_path = f"/en{path if path.startswith('/') else f'/{path}'}"

    return {
        "language_next_ru": f"{ru_path}{suffix}",
        "language_next_en": f"{en_path}{suffix}",
    }


def profile_preferences(request):
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return {
            "profile_preferences": profile,
            "active_theme": profile.theme,
        }
    return {
        "profile_preferences": None,
        "active_theme": "light",
    }
