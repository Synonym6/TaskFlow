from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title", "description", "color", "deadline", "is_archived")
        widgets = {
            "title": forms.TextInput(attrs={"autocomplete": "off"}),
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "color": forms.TextInput(attrs={"type": "color"}),
        }
        help_texts = {
            "is_archived": _("Архивные проекты остаются в системе, но не считаются активными."),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and not self.instance.pk and deadline < timezone.now():
            raise forms.ValidationError(_("Дедлайн проекта не должен быть в прошлом."))
        return deadline
