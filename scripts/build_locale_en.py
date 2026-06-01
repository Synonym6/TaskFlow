import re
from pathlib import Path

import polib


CYRILLIC_RANGE = "\\u0400-\\u04FF"
PATTERNS = [
    re.compile(r'_\(\s*["\']([^"\']*[' + CYRILLIC_RANGE + r'][^"\']*)["\']\s*\)'),
    re.compile(r'\{%\s*trans\s+["\']([^"\']*[' + CYRILLIC_RANGE + r'][^"\']*)["\']\s*%\}'),
]


TRANSLATIONS = {
    "Перейти к содержимому": "Skip to content",
    "Основная навигация": "Main navigation",
    "Дашборд": "Dashboard",
    "Задачи": "Tasks",
    "Проекты": "Projects",
    "Календарь": "Calendar",
    "Статистика": "Statistics",
    "Теги": "Tags",
    "Уведомления": "Notifications",
    "Настройки": "Settings",
    "Выход": "Log out",
    "Закрыть меню": "Close menu",
    "Открыть меню": "Open menu",
    "Рабочее пространство": "Workspace",
    "Открыть профиль": "Open profile",
    "Владелец": "Owner",
    "Профиль и безопасность": "Profile and security",
    "Управляйте данными профиля, темой, языком интерфейса и параметрами безопасности в одном месте.": "Manage profile data, theme, interface language, and security settings in one place.",
    "Профиль": "Profile",
    "Изменения имени, email, языка, темы и уведомлений применяются к вашему аккаунту.": "Changes to name, email, language, theme, and notifications apply to your account.",
    "Сохранить изменения": "Save changes",
    "Безопасность": "Security",
    "Смените пароль и держите доступ к аккаунту под контролем.": "Change your password and keep account access under control.",
    "Сменить пароль": "Change password",
    "Как это работает": "How it works",
    "Тема и язык сохраняются в профиле. После следующего входа выбранные настройки будут применены автоматически.": "Theme and language are saved in your profile. The selected settings will be applied automatically on your next sign-in.",
    "Текущая логика сохранена": "Existing logic is preserved",
    "Настройки продолжают работать через существующую backend-логику без дополнительных зависимостей и без потери данных.": "Settings continue to use the existing backend logic without extra dependencies or data loss.",
    "Имя": "Name",
    "Пароль": "Password",
    "Повтор пароля": "Repeat password",
    "Я согласен с условиями": "I agree to the terms",
    "Запомнить меня": "Remember me",
    "Заполните все обязательные поля.": "Fill in all required fields.",
    "Неверный email или пароль.": "Invalid email or password.",
    "Аккаунт отключен.": "Account is disabled.",
    "Пользователь с таким email уже существует.": "A user with this email already exists.",
    "Пароли не совпадают.": "Passwords do not match.",
    "Этот email уже используется.": "This email is already in use.",
    "Удалить аватар": "Remove avatar",
    "Аватар": "Avatar",
    "Язык интерфейса": "Interface language",
    "Язык": "Language",
    "Тема": "Theme",
    "Уведомления включены": "Notifications enabled",
    "Русский": "Russian",
    "Светлая": "Light",
    "Темная": "Dark",
    "Пользователь": "User",
    "Создан": "Created",
    "Создана": "Created",
    "Создано": "Created",
    "Обновлен": "Updated",
    "Обновлена": "Updated",
    "Профили": "Profiles",
    "Профиль обновлен.": "Profile updated.",
    "Пароль изменен.": "Password changed.",
    "Вы вошли в аккаунт.": "You are signed in.",
    "Вы вышли из системы.": "You have signed out.",
    "Регистрация прошла успешно.": "Registration completed successfully.",
    "Поиск задач, проектов...": "Search tasks, projects...",
    "Нет данных для сравнения": "No comparison data",
    "Ближайшие задачи": "Upcoming tasks",
    "Все задачи": "All tasks",
    "Ближайших задач пока нет.": "No upcoming tasks yet.",
    "Прогресс задач": "Task progress",
    "Неделя": "Week",
    "Недостаточно данных для графика.": "Not enough data for the chart.",
    "выполнено": "completed",
    "Недавние задачи": "Recent tasks",
    "Задача": "Task",
    "Проект": "Project",
    "Статус": "Status",
    "Приоритет": "Priority",
    "Срок": "Due date",
    "Действия": "Actions",
    "Просрочено": "Overdue",
    "У вас пока нет задач. Создайте первую задачу.": "You do not have tasks yet. Create your first task.",
    "Активные проекты": "Active projects",
    "Новый проект": "New project",
    "Все проекты": "All projects",
    "Проектов пока нет.": "No projects yet.",
    "Активность": "Activity",
    "Вы": "You",
    "Вся активность": "All activity",
    "Активность появится после первых действий.": "Activity will appear after your first actions.",
    "Всего задач": "Total tasks",
    "В работе": "In progress",
    "Выполнено": "Completed",
    "Вот что происходит с вашими задачами сегодня.": "Here is what is happening with your tasks today.",
    "Доброе утро": "Good morning",
    "Добрый день": "Good afternoon",
    "Добрый вечер": "Good evening",
    "%(value)s%% с прошлого месяца": "%(value)s%% since last month",
    "Новые данные в этом месяце": "New data this month",
    "Календарь задач": "Task calendar",
    "Просматривайте дедлайны по месяцам, неделям и дням. Каждая ссылка ведёт к реальной задаче или созданию новой на выбранную дату.": "View deadlines by month, week, and day. Each link opens a real task or creates a new one for the selected date.",
    "Создать задачу": "Create task",
    "Выберите удобный режим просмотра и откройте задачи прямо из календаря.": "Choose a convenient view mode and open tasks directly from the calendar.",
    "Режим календаря": "Calendar view mode",
    "Месяц": "Month",
    "День": "Day",
    "Нет задач на выбранный период.": "No tasks for the selected period.",
    "Пн": "Mon",
    "Вт": "Tue",
    "Ср": "Wed",
    "Чт": "Thu",
    "Пт": "Fri",
    "Сб": "Sat",
    "Вс": "Sun",
    "Новая задача": "New task",
    "Редактировать задачу": "Edit task",
    "Создать проект": "Create project",
    "Сохранить": "Save",
    "Отмена": "Cancel",
    "Удалить": "Delete",
    "Редактировать": "Edit",
    "Фильтры": "Filters",
    "Поиск": "Search",
    "Сбросить": "Reset",
    "Список задач": "Task list",
    "Быстрое создание": "Quick create",
    "Задачи не найдены": "No tasks found",
    "Без проекта": "No project",
    "Все статусы": "All statuses",
    "Все приоритеты": "All priorities",
    "Все теги": "All tags",
    "Все сроки": "All due dates",
    "Без сортировки": "No sorting",
    "Просроченные": "Overdue",
    "Сортировка": "Sort",
    "Применить": "Apply",
    "Название": "Title",
    "Описание": "Description",
    "Цвет": "Color",
    "Дедлайн": "Deadline",
    "Низкий": "Low",
    "Средний": "Medium",
    "Высокий": "High",
    "К выполнению": "To do",
    "Тестирование": "Testing",
    "Готово": "Done",
    "Комментарий": "Comment",
    "Комментарии": "Comments",
    "Чеклист": "Checklist",
    "Чеклисты": "Checklists",
    "Новый пункт": "New item",
    "Выполнен": "Completed",
    "Позиция": "Position",
    "Текст": "Text",
    "Автор": "Author",
    "Сообщение": "Message",
    "Тип": "Type",
    "Прочитано": "Read",
    "Системное": "System",
    "Скоро дедлайн": "Deadline soon",
    "Дедлайн сегодня": "Deadline today",
    "Задача выполнена": "Task completed",
    "Прогресс проекта": "Project progress",
    "Вход": "Sign in",
    "Войти": "Sign in",
    "Добро пожаловать!": "Welcome!",
    "Войдите в свой аккаунт": "Sign in to your account",
    "Забыли пароль?": "Forgot password?",
    "Нет аккаунта?": "No account?",
    "Зарегистрироваться": "Register",
    "Создание аккаунта": "Create account",
    "Создать аккаунт": "Create account",
    "Уже есть аккаунт?": "Already have an account?",
    "Регистрация": "Registration",
    "Восстановление пароля": "Password reset",
    "Вернуться ко входу": "Back to sign in",
    "Функция восстановления пароля будет добавлена позже.": "Password reset will be added later.",
    "Страница не найдена": "Page not found",
    "Что-то пошло не так": "Something went wrong",
}


def collect_strings():
    strings = {}
    for base in ("apps", "templates", "taskflow"):
        for path in Path(base).rglob("*"):
            if path.suffix not in {".py", ".html"} or "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in PATTERNS:
                for match in pattern.finditer(text):
                    strings.setdefault(match.group(1), set()).add(str(path))
    return strings


def main():
    strings = collect_strings()
    locale_dir = Path("locale/en/LC_MESSAGES")
    locale_dir.mkdir(parents=True, exist_ok=True)

    po = polib.POFile()
    po.metadata = {
        "Project-Id-Version": "TaskFlow 1.0",
        "Language": "en",
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
    }
    for msgid in sorted(strings):
        entry = polib.POEntry(msgid=msgid, msgstr=TRANSLATIONS.get(msgid, ""))
        for occurrence in sorted(strings[msgid]):
            entry.occurrences.append((occurrence, ""))
        po.append(entry)

    po.save(locale_dir / "django.po")
    po.save_as_mofile(locale_dir / "django.mo")
    translated = sum(1 for entry in po if entry.msgstr)
    print(f"entries={len(po)} translated={translated}")


if __name__ == "__main__":
    main()
