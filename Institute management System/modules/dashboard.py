import customtkinter as ctk
from config import COLORS
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DashboardModule:
    def __init__(self, app):
        self.app = app

    # ================= MAIN VIEW =================

    def show(self):
        for w in self.app.main_content.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self.app.main_content, fg_color="transparent", height=80)
        header.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="📊 Dashboard Overview",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="🔄 Refresh",
            fg_color=COLORS["info"],
            command=self.show
        ).pack(side="right")

        stats = self.app.db.get_dashboard_stats()

        self._stats_cards(stats)
        self._charts(stats)

    # ================= STATS =================

    def _stats_cards(self, stats):
        cards = ctk.CTkFrame(self.app.main_content, fg_color="transparent")
        cards.pack(fill="x", padx=30, pady=10)

        self._card(cards, "👨‍🎓 Students", stats.get("total_students", 0), COLORS["info"], 0)
        self._card(cards, "📚 Courses", stats.get("total_courses", 0), COLORS["success"], 1)
        self._card(cards, "📈 Attendance", f"{stats.get('attendance_rate', 0)}%", COLORS["warning"], 2)
        self._card(cards, "✅ Active", stats.get("active_students", 0), COLORS["secondary"], 3)

    def _card(self, parent, title, value, color, col):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=color)
        card.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack(pady=(5, 20))

    # ================= CHARTS =================

    def _charts(self, stats):
        container = ctk.CTkScrollableFrame(self.app.main_content)
        container.pack(fill="both", expand=True, padx=30, pady=20)

        self._pie_chart(container, stats.get("students_by_course", []))
        self._line_chart(container, stats.get("monthly_admissions", []))

    def _pie_chart(self, parent, data):
        frame = ctk.CTkFrame(parent, corner_radius=15)
        frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            frame,
            text="Students by Course",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        if data:
            labels = [d["course_name"] for d in data]
            sizes = [d["count"] for d in data]
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        else:
            ax.text(0.5, 0.5, "No data", ha="center", va="center")

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    def _line_chart(self, parent, data):
        frame = ctk.CTkFrame(parent, corner_radius=15)
        frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            frame,
            text="Monthly Admissions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        fig = Figure(figsize=(10, 4), dpi=100)
        ax = fig.add_subplot(111)

        if data:
            months = [d["month"] for d in data]
            counts = [d["count"] for d in data]
            ax.plot(months, counts, marker="o")
        else:
            ax.text(0.5, 0.5, "No data", ha="center", va="center")

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
