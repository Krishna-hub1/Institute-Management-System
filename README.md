# Institute Management System - Corrected Modular Version

This version is split from the original enhanced application without removing its UI/features.

## Modules

- `main.py` - application launcher
- `app.py` - application class and initialization
- `base_app.py` - shared window layout, sidebar, navigation and logout
- `db.py` - MySQL database layer
- `config.py` - database, SMTP, colors and paths
- `utils.py` - small filesystem helper
- `charts.py` - chart/stat-card methods
- `modules/auth.py` - login, registration and password reset
- `modules/dashboard.py` - dashboard UI
- `modules/students.py` - student management and profile dialogs
- `modules/courses.py` - course management
- `modules/attendance.py` - attendance management
- `modules/reports.py` - Excel exports and reports

## Important corrections

1. MySQL database names containing spaces are quoted correctly.
2. The `attendance.remarks` column is created and is also added automatically to an older existing attendance table if missing.
3. Gmail SMTP host is corrected to `smtp.gmail.com`.
4. The original enhanced UI, navigation, charts, filters, student dialogs, course dialogs, attendance screens and Excel exports are preserved.

## Run

1. Install dependencies:
   `pip install -r requirements.txt`
2. Set the MySQL password in `config.py`.
3. Run:
   `python main.py`
