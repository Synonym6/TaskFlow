from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    class LanguageChoices(models.TextChoices):
        RU = "ru", _("Русский")
        EN = "en", _("English")

    class ThemeChoices(models.TextChoices):
        LIGHT = "light", _("Светлая")
        DARK = "dark", _("Темная")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Пользователь"),
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name=_("Аватар"),
    )
    language = models.CharField(
        max_length=10,
        choices=LanguageChoices.choices,
        default=LanguageChoices.RU,
        verbose_name=_("Язык"),
    )
    theme = models.CharField(
        max_length=10,
        choices=ThemeChoices.choices,
        default=ThemeChoices.LIGHT,
        verbose_name=_("Тема"),
    )
    notifications_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Уведомления включены"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлен"))

    class Meta:
        verbose_name = _("Профиль")
        verbose_name_plural = _("Профили")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
