from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.projects.models import Project

from .models import ChecklistItem, Comment, SubTask, Tag, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "project", "status", "priority", "deadline", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"autocomplete": "off"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        help_texts = {
            "deadline": _("Новая задача не может получить прошедший дедлайн, если она ещё не завершена."),
            "tags": _("Можно выбрать несколько тегов текущего пользователя."),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["project"].queryset = Project.objects.filter(owner=self.user)
            self.fields["tags"].queryset = Tag.objects.filter(owner=self.user)

    def clean_project(self):
        project = self.cleaned_data.get("project")
        if project and project.owner != self.user:
            raise forms.ValidationError(_("Нельзя использовать чужой проект."))
        return project

    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        for tag in tags:
            if tag.owner != self.user:
                raise forms.ValidationError(_("Нельзя прикрепить чужой тег."))
        return tags

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        status = self.cleaned_data.get("status") or self.instance.status or Task.StatusChoices.TODO
        if not deadline:
            return deadline
        if self.instance.pk:
            previous_deadline = self.instance.deadline
            if deadline < timezone.now() and status != Task.StatusChoices.DONE:
                if previous_deadline != deadline and (previous_deadline is None or previous_deadline >= timezone.now()):
                    raise forms.ValidationError(_("Нельзя установить новый дедлайн в прошлом."))
            return deadline
        if deadline < timezone.now() and status != Task.StatusChoices.DONE:
            raise forms.ValidationError(_("Нельзя создать задачу с дедлайном в прошлом."))
        return deadline

    def save(self, commit=True):
        task = super().save(commit=False)
        task.owner = self.user
        if commit:
            task.save()
            self.save_m2m()
        return task


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", "color")
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        exists = Tag.objects.filter(owner=self.user, name__iexact=name).exclude(pk=self.instance.pk).exists()
        if exists:
            raise forms.ValidationError(_("Такой тег уже существует."))
        return name

    def save(self, commit=True):
        tag = super().save(commit=False)
        tag.owner = self.user
        if commit:
            tag.save()
        return tag


class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ("text",)
        labels = {"text": _("Новый пункт")}
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": _("Добавьте новый пункт чек-листа")}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        labels = {"text": _("Комментарий")}
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": _("Напишите комментарий...")}),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ("title", "deadline")
        labels = {
            "title": _("Подзадача"),
            "deadline": _("Срок"),
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": _("Название подзадачи")}),
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class TaskMetaForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("status", "priority")


class TaskTagAddForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tag.objects.none(), empty_label=None, label=_("Тег"))

    def __init__(self, *args, user=None, task=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Tag.objects.filter(owner=user) if user else Tag.objects.none()
        if task is not None:
            queryset = queryset.exclude(tasks=task)
        self.fields["tag"].queryset = queryset.order_by("name")
