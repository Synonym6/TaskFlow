# TaskFlow

TaskFlow is an alpha-version Django web application for managing tasks, projects, deadlines, notifications and analytics.

## Stack

- Python
- Django
- SQLite
- Django Templates
- HTML / CSS / JavaScript
- Chart.js
- SortableJS
- Django Admin

## Features

- Registration and login by email
- Personal dashboard with real counters and charts
- Task CRUD with filters, sorting and detail page
- Projects with progress calculation from real tasks
- Kanban board with drag-and-drop and backend validation
- Calendar with real deadlines
- Statistics page with Chart.js
- Tags, comments, checklist and activity log
- Notifications based on task and project state
- Light and dark theme
- Russian and English user interface
- Django Admin configured in Russian
- Superuser self-protection in admin

## 1. Install Python

If `python` is not available on your system, install Python 3.12 or newer.

Windows options:

1. From the official website:
   https://www.python.org/downloads/windows/
2. Or with `winget`:

```powershell
winget install -e --id Python.Python.3.12
```

After installation, reopen VS Code terminal and verify:

```powershell
python --version
pip --version
```

## 2. Open the project folder

```powershell
cd C:\Users\Synonym\Desktop\преддипломка\taskflow
```

## 3. Create a virtual environment

```powershell
python -m venv venv
```

## 4. Activate the virtual environment

```powershell
venv\Scripts\activate
```

## 5. Install dependencies

```powershell
pip install -r requirements.txt
```

## 6. Create migrations

```powershell
python manage.py makemigrations
```

## 7. Apply migrations

```powershell
python manage.py migrate
```

## 8. Create a superuser

```powershell
python manage.py createsuperuser
```

## 9. Run the development server

```powershell
python manage.py runserver
```

For access from another device in the same home Wi-Fi network, run:

```powershell
python manage.py runserver 0.0.0.0:8000
```

## 10. Open the application

- Website: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Optional: create demo data

This command is optional and not required for application logic:

```powershell
python manage.py seed_demo_data
```

## Demo account for testing

After running `python manage.py seed_demo_data`, you can log into the ready-made test account:

- Email: `demo@taskflow.local`
- Password: `TaskFlowDemo123!`

This demo account already contains:

- 4 projects
- 12 tasks in different statuses
- 1 overdue task
- 3 completed tasks
- 6 tags
- checklist items
- comments
- notifications
- activity log entries

It is intended for quick manual testing of dashboard, Kanban, calendar, statistics, notifications and task detail pages without filling the system manually.

## Project structure

```text
taskflow/
  manage.py
  taskflow/
    settings.py
    urls.py
    wsgi.py
    asgi.py
  apps/
    accounts/
    tasks/
    projects/
    dashboard/
    notifications/
  templates/
  static/
    css/
    js/
    img/
  locale/
  requirements.txt
  README.md
```

## Notes

- Database engine: SQLite (`db.sqlite3`)
- Theme is stored in profile and also mirrored in `localStorage`
- Interface languages: Russian and English
- Admin is forced to Russian
- Notifications, dashboard metrics, Kanban, calendar and charts are based on current user data
- Password reset page is an honest placeholder in this alpha version

## VS Code

Recommended steps:

1. Open the `taskflow` folder in VS Code.
2. Select the interpreter from `venv`.
3. Run commands in the integrated terminal.
4. Start the server with `python manage.py runserver`.

## Local network access from phone or tablet

This is only for local testing inside the same home Wi-Fi network. It is not a production deployment.

Steps:

1. Connect the PC and the phone/tablet to the same Wi-Fi network.
2. Check the IPv4 address of the active Wi-Fi adapter:

```powershell
ipconfig
```

3. Find the `IPv4 Address` of the active Wi-Fi adapter.
   Current example on this PC: `192.168.0.20`
4. Make sure this IP is listed in `ALLOWED_HOSTS` in `taskflow/settings.py`.
5. Start the server so Django listens on the local network:

```powershell
python manage.py runserver 0.0.0.0:8000
```

6. Open the project on the phone:

```text
http://192.168.0.20:8000/
```

Detailed guide:

- `docs/local-network.md`

## Local network diagnostics

If the site does not open from the phone, check:

- the phone and PC are in the same Wi-Fi network;
- Windows Firewall is not blocking port `8000`;
- Python/Django is allowed on private networks;
- the PC IP address did not change;
- Django was started on `0.0.0.0:8000`, not `127.0.0.1:8000`;
- the current local IP is added to `ALLOWED_HOSTS`.

## Important

The current workspace originally had no working `python` or `pip` in PATH, so if commands fail, install Python first and then repeat the steps above.
