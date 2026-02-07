import customtkinter as ctk
from tkinter import messagebox

# ---------------- APPEARANCE ----------------
ctk.set_appearance_mode("light")      # "dark" if you prefer
ctk.set_default_color_theme("blue")

# ---------------- CORE ----------------
from db import Database
from config import COLORS

# ---------------- MODULES ----------------
from modules.auth import AuthModule
from modules.dashboard import DashboardModule
from modules.students import StudentsModule
from modules.courses import CoursesModule
from modules.attendance import AttendanceModule
from modules.reports import ReportsModule


class StudentManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -------- Window --------
        self.title("Institute Management System")
        self.geometry("1280x680+0+5")

        # -------- Database --------
        self.db = Database()
        if not self.db.initialize_database():
            messagebox.showerror("Database Error", "Failed to initialize database!")
            self.destroy()
            return

        # -------- App State --------
        self.current_user = None
        self.current_section = None

        # -------- Layout --------
        self.sidebar = None
        self.main_content = None

        # -------- Modules --------
        self.auth = AuthModule(self)
        self.dashboard = DashboardModule(self)
        self.students = StudentsModule(self)
        self.courses = CoursesModule(self)
        self.attendance = AttendanceModule(self)
        self.reports = ReportsModule(self)

        # -------- Start App --------
        self.auth.show_login_screen()

    # ======================================================
    # LAYOUT HELPERS
    # ======================================================

    def clear_window(self):
        """Remove all widgets from root window"""
        for widget in self.winfo_children():
            widget.destroy()

    def build_main_layout(self):
        """Create sidebar + main content layout"""
        self.clear_window()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=COLORS["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main content
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="right", fill="both", expand=True)

        self._sidebar_buttons()
        self.show_dashboard()

    # ======================================================
    # SIDEBAR
    # ======================================================

    def _sidebar_buttons(self):
        """Create sidebar navigation buttons"""

        nav_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👨‍🎓 Students", self.students.show),
            ("📚 Courses", self.courses.show),
            ("📝 Attendance", self.attendance.show),
            ("📈 Reports", self.reports.show),
        ]

        for text, command in nav_items:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                height=45,
                anchor="w",
                fg_color="transparent",
                hover_color=COLORS["sidebar_hover"],
                command=command
            ).pack(fill="x", padx=15, pady=5)

        # Logout button
        ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            height=45,
            fg_color=COLORS["danger"],
            hover_color="#c0392b",
            command=self.logout
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    # ======================================================
    # NAVIGATION
    # ======================================================

    def show_dashboard(self):
        if self.main_content:
            self.dashboard.show()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.auth.show_login_screen()
