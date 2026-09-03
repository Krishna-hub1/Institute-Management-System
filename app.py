import customtkinter as ctk
from tkinter import messagebox

from db import Database
from config import COLORS

from modules.auth import AuthModule
from modules.dashboard import DashboardModule
from modules.charts import ChartsModule
from modules.students import StudentsModule
from modules.courses import CoursesModule
from modules.attendance import AttendanceModule
from modules.reports import ReportsModule
from base_app import BaseApp


APP_SHORT_NAME = "BMK"
APP_FULL_NAME = "Institute Management System"
APP_TAGLINE = "Smart Institute Administration"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class StudentManagementSystem(
    AuthModule,
    DashboardModule,
    ChartsModule,
    StudentsModule,
    CoursesModule,
    AttendanceModule,
    ReportsModule,
    BaseApp,
):
    def __init__(self):
            super().__init__()

            # Window configuration
            self.title('Institute Management System')
            self.geometry("1280x680+0+5")

            # Initialize database
            self.db = Database()
            if not self.db.initialize_database():
                messagebox.showerror("Database Error", "Failed to initialize database!")
                self.destroy()
                return

            # Variables
            self.current_user = None
            self.current_section = "Dashboard"
            self.selected_photo_path = None
            self.photo_preview_label = None

            # Show login screen first
            self.show_login_screen()

if __name__ == "__main__":
    app = StudentManagementSystem()
    app.mainloop()
