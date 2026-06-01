from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Profile


User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        label=_("Пароль"),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        label=_("Повтор пароля"),
    )
    agree_terms = forms.BooleanField(label=_("Я согласен с условиями"))

    class Meta:
        model = User
        fields = ("first_name", "email")
        labels = {
            "first_name": _("Имя"),
            "email": _("Email"),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("Пользователь с таким email уже существует."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", _("Пароли не совпадают."))
        if password1:
            password_validation.validate_password(password1)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        label=_("Пароль"),
    )
    remember_me = forms.BooleanField(required=False, label=_("Запомнить меня"))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if not email or not password:
            raise ValidationError(_("Заполните все обязательные поля."))
        self.user_cache = authenticate(self.request, username=email, password=password)
        if self.user_cache is None:
            raise ValidationError(_("Неверный email или пароль."))
        if not self.user_cache.is_active:
            raise ValidationError(_("Аккаунт отключен."))
        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "email")
        labels = {
            "first_name": _("Имя"),
            "email": _("Email"),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        exists = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists()
        if exists:
            raise ValidationError(_("Этот email уже используется."))
        return email


class ProfilePreferencesForm(forms.ModelForm):
    remove_avatar = forms.BooleanField(required=False, label=_("Удалить аватар"))

    class Meta:
        model = Profile
        fields = ("avatar", "language", "theme", "notifications_enabled")
        labels = {
            "avatar": _("Аватар"),
            "language": _("Язык интерфейса"),
            "theme": _("Тема"),
            "notifications_enabled": _("Уведомления"),
        }


class SecurityPasswordForm(PasswordChangeForm):
    pass
