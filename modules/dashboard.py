import customtkinter as ctk

from config import COLORS



class DashboardModule:
    """Feature module extracted from the original application."""

    def show_dashboard(self):
            """Display dashboard with statistics and charts"""
            # Header
            header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=80)
            header.pack(fill="x", padx=30, pady=(20, 10))

            title = ctk.CTkLabel(
                header,
                text="📊 Dashboard Overview",
                font=ctk.CTkFont(size=28, weight="bold")
            )
            title.pack(side="left")

            refresh_btn = ctk.CTkButton(
                header,
                text="🔄 Refresh",
                width=120,
                height=40,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLORS["info"],
                command=lambda: self.navigate_to("Dashboard")
            )
            refresh_btn.pack(side="right")

            # Get statistics
            stats = self.db.get_dashboard_stats()

            # Stats Cards Row
            cards_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
            cards_frame.pack(fill="x", padx=30, pady=10)

            # Create stat cards
            self.create_stat_card(cards_frame, "👨‍🎓 Total Students",
                                  stats.get('total_students', 0), COLORS["info"], 0)
            self.create_stat_card(cards_frame, "📚 Total Courses",
                                  stats.get('total_courses', 0), COLORS["success"], 1)
            self.create_stat_card(cards_frame, "📈 Attendance Rate",
                                  f"{stats.get('attendance_rate', 0)}%", COLORS["warning"], 2)
            self.create_stat_card(cards_frame, "✅ Active Students",
                                  stats.get('active_students', 0), COLORS["secondary"], 3)

            # Charts Section
            charts_container = ctk.CTkScrollableFrame(self.main_content)
            charts_container.pack(fill="both", expand=True, padx=30, pady=20)

            # Row 1: Pie Chart and Bar Chart
            row1 = ctk.CTkFrame(charts_container, fg_color="transparent")
            row1.pack(fill="x", pady=10)

            # Pie Chart - Students by Course
            pie_frame = ctk.CTkFrame(row1, corner_radius=15)
            pie_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

            pie_title = ctk.CTkLabel(pie_frame, text="Students Distribution by Course",
                                     font=ctk.CTkFont(size=16, weight="bold"))
            pie_title.pack(pady=15)

            self.create_pie_chart(pie_frame, stats.get('students_by_course', []))

            # Bar Chart - Attendance by Course
            bar_frame = ctk.CTkFrame(row1, corner_radius=15)
            bar_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

            bar_title = ctk.CTkLabel(bar_frame, text="Attendance Rate by Course",
                                     font=ctk.CTkFont(size=16, weight="bold"))
            bar_title.pack(pady=15)

            self.create_attendance_bar_chart(bar_frame)

            # Row 2: Line Chart - Monthly Admissions
            row2 = ctk.CTkFrame(charts_container, fg_color="transparent")
            row2.pack(fill="x", pady=10)

            line_frame = ctk.CTkFrame(row2, corner_radius=15)
            line_frame.pack(fill="both", expand=True)

            line_title = ctk.CTkLabel(line_frame, text="Monthly Admission Trends (Last 12 Months)",
                                      font=ctk.CTkFont(size=16, weight="bold"))
            line_title.pack(pady=15)

            self.create_line_chart(line_frame, stats.get('monthly_admissions', []))
