import customtkinter as ctk
from tkinter import messagebox

from config import COLORS


class BaseApp(ctk.CTk):
    """Shared application layout and navigation."""

    def show_main_application(self):
            """Display main application interface"""
            # Clear window
            for widget in self.winfo_children():
                widget.destroy()

            # Create main layout
            # Sidebar
            self.sidebar = ctk.CTkFrame(
                self,
                width=250,
                corner_radius=0,
                fg_color=COLORS["sidebar"]
            )
            self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
            self.sidebar.pack_propagate(False)

            # Main content area
            self.main_content = ctk.CTkFrame(self, corner_radius=0)
            self.main_content.pack(side="right", fill="both", expand=True, padx=0, pady=0)

            self.create_sidebar()
            self.show_dashboard()

    def create_sidebar(self):
            """Create navigation sidebar"""
            # Logo/Title
            logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            logo_frame.pack(pady=30, padx=20)

            logo_label = ctk.CTkLabel(
                logo_frame,
                text="BMK",
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color=COLORS["success"]
            )
            logo_label.pack()

            subtitle = ctk.CTkLabel(
                logo_frame,
                text="Institute Management",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            subtitle.pack()

            # User info
            user_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["sidebar_hover"], corner_radius=10)
            user_frame.pack(pady=20, padx=15, fill="x")

            user_label = ctk.CTkLabel(
                user_frame,
                text=f"👤 {self.current_user['full_name']}",
                font=ctk.CTkFont(size=13, weight="bold")
           
            )
            user_label.pack(pady=8)

            role_label = ctk.CTkLabel(
                user_frame,
                text=f"Role: {self.current_user['role']}",
                font=ctk.CTkFont(size=11),
                text_color="black"
            )
            role_label.pack(pady=(0, 8))

            # Navigation buttons
            self.nav_buttons = {}
            nav_items = [
                ("📊 Dashboard", "Dashboard"),
                ("👨‍🎓 Students", "Students"),
                ("📚 Courses", "Courses"),
                ("📝 Attendance", "Attendance"),
                ("📈 Reports", "Reports"),
            ]

            for text, section in nav_items:
                btn = ctk.CTkButton(
                    self.sidebar,
                    text=text,
                    font=ctk.CTkFont(size=14),
                    height=45,
                    corner_radius=10,
                    fg_color="transparent",
                    text_color="white",
                    hover_color=COLORS["sidebar_hover"],
                    anchor="w",
                    command=lambda s=section: self.navigate_to(s)
                )
                btn.pack(pady=5, padx=15, fill="x")
                self.nav_buttons[section] = btn

            # Highlight current section
            self.highlight_nav_button("Dashboard")

            # Logout button at bottom
            logout_btn = ctk.CTkButton(
                self.sidebar,
                text="🚪 Logout",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=45,
                corner_radius=10,
                fg_color=COLORS["danger"],
                hover_color="#c0392b",
                command=self.logout
            )
            logout_btn.pack(side="bottom", pady=20, padx=15, fill="x")

    def highlight_nav_button(self, section):
            """Highlight the active navigation button"""
            for sec, btn in self.nav_buttons.items():
                if sec == section:
                    btn.configure(fg_color=COLORS["primary"], font=ctk.CTkFont(size=14, weight="bold"))
                else:
                    btn.configure(fg_color="transparent", font=ctk.CTkFont(size=14))

    def navigate_to(self, section):
            """Navigate to different sections"""
            self.current_section = section
            self.highlight_nav_button(section)

            # Clear main content
            for widget in self.main_content.winfo_children():
                widget.destroy()

            # Show appropriate section
            if section == "Dashboard":
                self.show_dashboard()
            elif section == "Students":
                self.show_students()
            elif section == "Courses":
                self.show_courses()
            elif section == "Attendance":
                self.show_attendance()
            elif section == "Reports":
                self.show_reports()

    def logout(self):
            """Logout user"""
            if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
                self.current_user = None
                self.show_login_screen()
