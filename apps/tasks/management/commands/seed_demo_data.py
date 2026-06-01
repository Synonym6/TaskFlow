from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.notifications.models import Notification
from apps.projects.models import Project
from apps.tasks.models import ActivityLog, ChecklistItem, Comment, Tag, Task


class Command(BaseCommand):
    help = "Creates a reusable demo account with filled projects, tasks, comments, checklist items and notifications."

    def handle(self, *args, **options):
        now = timezone.now()
        user_model = get_user_model()

        user, created = user_model.objects.get_or_create(
            email="demo@taskflow.local",
            defaults={
                "username": "demo@taskflow.local",
                "first_name": "Demo",
                "last_name": "User",
                "is_active": True,
            },
        )
        user.username = "demo@taskflow.local"
        user.first_name = "Demo"
        user.last_name = "User"
        user.set_password("TaskFlowDemo123!")
        user.save()

        profile = user.profile
        profile.language = "ru"
        profile.theme = "light"
        profile.notifications_enabled = True
        profile.save()

        Notification.objects.filter(owner=user).delete()
        ActivityLog.objects.filter(owner=user).delete()
        Comment.objects.filter(author=user).delete()
        ChecklistItem.objects.filter(task__owner=user).delete()
        Task.objects.filter(owner=user).delete()
        Tag.objects.filter(owner=user).delete()
        Project.objects.filter(owner=user).delete()

        project_specs = [
            {
                "title": "Преддипломная практика",
                "description": "Ключевой проект для отчета, аналитики и демонстрации TaskFlow.",
                "color": "#6f61ff",
                "deadline": now + timedelta(days=12),
            },
            {
                "title": "Учеба",
                "description": "Домашние задания, подготовка к зачетам и учебный план.",
                "color": "#4f7cff",
                "deadline": now + timedelta(days=25),
            },
            {
                "title": "Работа",
                "description": "Операционные задачи, тестирование и встречи по проектам.",
                "color": "#23b26d",
                "deadline": now + timedelta(days=8),
            },
            {
                "title": "Личное",
                "description": "Личные дела и бытовые задачи для полноты тестового аккаунта.",
                "color": "#ff7a59",
                "deadline": now + timedelta(days=18),
            },
        ]

        projects = {}
        for spec in project_specs:
            project = Project.objects.create(owner=user, **spec)
            projects[spec["title"]] = project

        tag_specs = [
            ("Срочно", "#f25572"),
            ("Дизайн", "#6f61ff"),
            ("Документы", "#4f7cff"),
            ("Идея", "#8f75ff"),
            ("Frontend", "#22b8cf"),
            ("Backend", "#23b26d"),
        ]
        tags = {name: Tag.objects.create(owner=user, name=name, color=color) for name, color in tag_specs}

        task_specs = [
            {
                "title": "Подготовить отчет по практике",
                "description": "Собрать структуру отчета, обновить аналитический раздел и финальные выводы.",
                "project": projects["Преддипломная практика"],
                "status": Task.StatusChoices.IN_PROGRESS,
                "priority": Task.PriorityChoices.HIGH,
                "deadline": now + timedelta(hours=18),
                "position": 0,
                "tags": ["Срочно", "Документы"],
            },
            {
                "title": "Сверстать landing page",
                "description": "Доработать hero-блок, карточки преимуществ и адаптивность мобильной версии.",
                "project": projects["Преддипломная практика"],
                "status": Task.StatusChoices.TESTING,
                "priority": Task.PriorityChoices.MEDIUM,
                "deadline": now + timedelta(days=2),
                "position": 0,
                "tags": ["Frontend", "Дизайн"],
            },
            {
                "title": "Исправить фильтрацию задач",
                "description": "Проверить backend-валидацию и логику сортировки по приоритету и дедлайну.",
                "project": projects["Работа"],
                "status": Task.StatusChoices.TODO,
                "priority": Task.PriorityChoices.HIGH,
                "deadline": now + timedelta(days=1, hours=5),
                "position": 0,
                "tags": ["Backend", "Срочно"],
            },
            {
                "title": "Провести code review",
                "description": "Проверить модуль проектов, уведомлений и права доступа обычного пользователя.",
                "project": projects["Работа"],
                "status": Task.StatusChoices.DONE,
                "priority": Task.PriorityChoices.MEDIUM,
                "deadline": now - timedelta(days=1),
                "position": 0,
                "tags": ["Backend"],
            },
            {
                "title": "Подготовиться к защите",
                "description": "Собрать речь, продумать демонстрационный сценарий и ответы на вопросы.",
                "project": projects["Учеба"],
                "status": Task.StatusChoices.IN_PROGRESS,
                "priority": Task.PriorityChoices.HIGH,
                "deadline": now + timedelta(days=4),
                "position": 1,
                "tags": ["Документы", "Срочно"],
            },
            {
                "title": "Оформить презентацию",
                "description": "Сделать лаконичные слайды по функционалу приложения и архитектуре.",
                "project": projects["Учеба"],
                "status": Task.StatusChoices.TODO,
                "priority": Task.PriorityChoices.MEDIUM,
                "deadline": now + timedelta(days=6),
                "position": 1,
                "tags": ["Дизайн", "Документы"],
            },
            {
                "title": "Записаться к научному руководителю",
                "description": "Уточнить время консультации и список замечаний по практике.",
                "project": projects["Учеба"],
                "status": Task.StatusChoices.DONE,
                "priority": Task.PriorityChoices.LOW,
                "deadline": now - timedelta(days=3),
                "position": 1,
                "tags": ["Идея"],
            },
            {
                "title": "Оплатить интернет",
                "description": "Бытовая задача для проверки личного проекта и карточек на dashboard.",
                "project": projects["Личное"],
                "status": Task.StatusChoices.TODO,
                "priority": Task.PriorityChoices.LOW,
                "deadline": now + timedelta(days=3),
                "position": 2,
                "tags": ["Идея"],
            },
            {
                "title": "Проверить просроченные задачи",
                "description": "Тестовая просроченная задача для проверки красных статусов и уведомлений.",
                "project": projects["Преддипломная практика"],
                "status": Task.StatusChoices.TODO,
                "priority": Task.PriorityChoices.HIGH,
                "deadline": now + timedelta(days=1),
                "force_overdue_deadline": now - timedelta(hours=10),
                "position": 2,
                "tags": ["Срочно", "Backend"],
            },
            {
                "title": "Настроить уведомления",
                "description": "Проверить отображение уведомлений и статус прочтения.",
                "project": projects["Работа"],
                "status": Task.StatusChoices.TESTING,
                "priority": Task.PriorityChoices.MEDIUM,
                "deadline": now + timedelta(hours=7),
                "position": 1,
                "tags": ["Backend", "Frontend"],
            },
            {
                "title": "Собрать аналитику по проектам",
                "description": "Сверить статистику по статусам, приоритетам и прогрессу проектов.",
                "project": projects["Преддипломная практика"],
                "status": Task.StatusChoices.DONE,
                "priority": Task.PriorityChoices.MEDIUM,
                "deadline": now - timedelta(days=2),
                "position": 1,
                "tags": ["Документы", "Backend"],
            },
            {
                "title": "Подготовить идеи для следующего релиза",
                "description": "Список улучшений для настроек, мобильного меню и UX карточек.",
                "project": projects["Личное"],
                "status": Task.StatusChoices.IN_PROGRESS,
                "priority": Task.PriorityChoices.LOW,
                "deadline": now + timedelta(days=9),
                "position": 2,
                "tags": ["Идея", "Дизайн"],
            },
        ]

        created_tasks = {}
        for spec in task_specs:
            task = Task.objects.create(
                owner=user,
                title=spec["title"],
                description=spec["description"],
                project=spec["project"],
                status=spec["status"],
                priority=spec["priority"],
                deadline=spec["deadline"],
                position=spec["position"],
            )
            task.tags.set([tags[name] for name in spec["tags"]])
            if "force_overdue_deadline" in spec:
                Task.objects.filter(pk=task.pk).update(deadline=spec["force_overdue_deadline"])
                task.refresh_from_db()
            if task.status == Task.StatusChoices.DONE and task.deadline:
                task.completed_at = task.deadline - timedelta(hours=2)
                task.save(update_fields=["completed_at", "updated_at"])
            created_tasks[task.title] = task

        checklist_specs = {
            "Подготовить отчет по практике": [
                ("Собрать данные по проекту", True),
                ("Обновить диаграммы", True),
                ("Оформить введение", False),
                ("Проверить заключение", False),
            ],
            "Сверстать landing page": [
                ("Проверить hero-блок", True),
                ("Доработать анимации", False),
                ("Проверить mobile breakpoint", False),
            ],
            "Подготовиться к защите": [
                ("Собрать тезисы выступления", True),
                ("Проверить демонстрационный сценарий", False),
                ("Подготовить ответы на вопросы", False),
            ],
        }
        for task_title, items in checklist_specs.items():
            task = created_tasks[task_title]
            for index, (text, is_done) in enumerate(items):
                ChecklistItem.objects.create(task=task, text=text, is_done=is_done, position=index)

        comment_specs = {
            "Подготовить отчет по практике": [
                "Добавил замечания по аналитической части и структуре разделов.",
                "Нужно отдельно перепроверить сроки и список источников.",
            ],
            "Сверстать landing page": [
                "Hero выглядит лучше, но стоит проверить отступы на планшете.",
            ],
            "Исправить фильтрацию задач": [
                "После фикса нужно проверить сценарий с несколькими тегами.",
            ],
        }
        for task_title, comments in comment_specs.items():
            task = created_tasks[task_title]
            for text in comments:
                Comment.objects.create(task=task, author=user, text=text)

        log_specs = [
            ("Создан проект", "Создан проект Преддипломная практика", None, projects["Преддипломная практика"]),
            ("Создан проект", "Создан проект Учеба", None, projects["Учеба"]),
            ("Создана задача", "Создана задача Подготовить отчет по практике", created_tasks["Подготовить отчет по практике"], projects["Преддипломная практика"]),
            ("Создана задача", "Создана задача Сверстать landing page", created_tasks["Сверстать landing page"], projects["Преддипломная практика"]),
            ("Добавлен комментарий", "Добавлен комментарий к задаче Подготовить отчет по практике", created_tasks["Подготовить отчет по практике"], projects["Преддипломная практика"]),
            ("Обновлен статус", "Задача Провести code review переведена в статус Готово", created_tasks["Провести code review"], projects["Работа"]),
            ("Kanban обновлен", "Задача Настроить уведомления перемещена в Тестирование", created_tasks["Настроить уведомления"], projects["Работа"]),
        ]
        for action, description, task, project in log_specs:
            ActivityLog.objects.create(owner=user, action=action, description=description, task=task, project=project)

        notification_specs = [
            ("Дедлайн сегодня", "Задача \"Подготовить отчет по практике\" требует внимания сегодня.", Notification.NotificationType.DEADLINE_TODAY, created_tasks["Подготовить отчет по практике"], None, False),
            ("Скоро дедлайн", "До дедлайна задачи \"Настроить уведомления\" осталось меньше 24 часов.", Notification.NotificationType.DEADLINE_SOON, created_tasks["Настроить уведомления"], None, False),
            ("Задача просрочена", "Срок задачи \"Проверить просроченные задачи\" уже истек.", Notification.NotificationType.OVERDUE, created_tasks["Проверить просроченные задачи"], None, False),
            ("Прогресс проекта", "Проект \"Преддипломная практика\" достиг заметного прогресса.", Notification.NotificationType.PROJECT_PROGRESS, None, projects["Преддипломная практика"], True),
            ("Задача выполнена", "Задача \"Провести code review\" успешно завершена.", Notification.NotificationType.TASK_COMPLETED, created_tasks["Провести code review"], None, True),
        ]
        for title, message, n_type, related_task, related_project, is_read in notification_specs:
            Notification.objects.create(
                owner=user,
                title=title,
                message=message,
                type=n_type,
                related_task=related_task,
                related_project=related_project,
                is_read=is_read,
            )

        self.stdout.write(self.style.SUCCESS("Demo account refreshed successfully."))
        if created:
            self.stdout.write("Created new demo user: demo@taskflow.local / TaskFlowDemo123!")
        else:
            self.stdout.write("Updated existing demo user: demo@taskflow.local / TaskFlowDemo123!")
