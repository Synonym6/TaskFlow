from .models import Profile


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
