import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

from config import COLORS


class AttendanceModule:
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
            text="📝 Attendance Management",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="✅ Mark Attendance",
            fg_color=COLORS["success"],
            command=self.show_mark_attendance_dialog
        ).pack(side="right")

        self._filter_section()

    # ================= FILTER + VIEW =================

    def _filter_section(self):
        filter_frame = ctk.CTkFrame(self.app.main_content, fg_color="transparent")
        filter_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(filter_frame, text="Date:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        self.date_filter = DateEntry(
            filter_frame,
            background=COLORS["primary"],
            foreground="white",
            date_pattern="yyyy-mm-dd"
        )
        self.date_filter.pack(side="left", padx=5)

        courses = self.app.db.get_all_courses()
        self.course_map = {c["course_name"]: c["course_id"] for c in courses}
        course_names = ["All"] + list(self.course_map.keys())

        ctk.CTkLabel(filter_frame, text="Course:", font=ctk.CTkFont(size=12, weight="bold")).pack(
            side="left", padx=(20, 5)
        )
        self.course_filter = ctk.CTkOptionMenu(filter_frame, values=course_names)
        self.course_filter.pack(side="left", padx=5)

        ctk.CTkButton(
            filter_frame,
            text="View Records",
            command=self.view_attendance
        ).pack(side="left", padx=20)

        self.info_frame = ctk.CTkFrame(self.app.main_content, fg_color=COLORS["info"], corner_radius=15)
        self.info_frame.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(
            self.info_frame,
            text="📊 Attendance Tracking System\n\nSelect date and course to view records.",
            font=ctk.CTkFont(size=16),
            text_color="white"
        ).pack(expand=True, pady=50)

    def view_attendance(self):
        for w in self.info_frame.winfo_children():
            w.destroy()

        date = self.date_filter.get_date()
        selected_course = self.course_filter.get()
        course_id = self.course_map.get(selected_course) if selected_course != "All" else None

        records = self.app.db.get_attendance_by_date(date, course_id)

        ctk.CTkLabel(
            self.info_frame,
            text=f"📅 Attendance Records – {date}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=10)

        if not records:
            ctk.CTkLabel(
                self.info_frame,
                text="No attendance records found",
                font=ctk.CTkFont(size=16),
                text_color="white"
            ).pack(pady=40)
            return

        table = ctk.CTkScrollableFrame(self.info_frame)
        table.pack(fill="both", expand=True, padx=20, pady=10)

        headers = ["Student", "Course", "Status"]
        widths = [300, 250, 150]

        header_row = ctk.CTkFrame(table, fg_color=COLORS["primary"])
        header_row.pack(fill="x")

        for i, h in enumerate(headers):
            ctk.CTkLabel(
                header_row,
                text=h,
                width=widths[i],
                text_color="white",
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="center"
            ).grid(row=0, column=i, padx=1, pady=1)

        for r in records:
            row = ctk.CTkFrame(table)
            row.pack(fill="x")

            values = [
                f"{r['first_name']} {r['last_name']}",
                r["course_name"],
                r["status"]
            ]

            for i, v in enumerate(values):
                ctk.CTkLabel(
                    row,
                    text=v,
                    width=widths[i],
                    anchor="center"
                ).grid(row=0, column=i, padx=1, pady=1)

    # ================= MARK ATTENDANCE =================

    def show_mark_attendance_dialog(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Mark Attendance")
        dialog.geometry("650x600")
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="✅ Mark Attendance",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)

        select_frame = ctk.CTkFrame(dialog)
        select_frame.pack(padx=40, pady=10, fill="x")

        courses = self.app.db.get_all_courses()
        course_map = {c["course_name"]: c["course_id"] for c in courses}

        ctk.CTkLabel(select_frame, text="Course:").pack(side="left", padx=5)
        course_menu = ctk.CTkOptionMenu(select_frame, values=list(course_map.keys()))
        course_menu.pack(side="left", padx=5)

        ctk.CTkLabel(select_frame, text="Date:").pack(side="left", padx=10)
        date_entry = DateEntry(select_frame, date_pattern="yyyy-mm-dd")
        date_entry.pack(side="left", padx=5)

        student_frame = ctk.CTkScrollableFrame(dialog, height=350)
        student_frame.pack(fill="both", expand=True, padx=40, pady=10)

        attendance_vars = []

        def load_students():
            for w in student_frame.winfo_children():
                w.destroy()
            attendance_vars.clear()

            course_id = course_map.get(course_menu.get())
            students = [s for s in self.app.db.get_all_students() if s["course_id"] == course_id]

            for s in students:
                row = ctk.CTkFrame(student_frame)
                row.pack(fill="x", pady=5)

                ctk.CTkLabel(
                    row,
                    text=f"{s['first_name']} {s['last_name']} ({s['student_id']})",
                    width=300,
                    anchor="w"
                ).pack(side="left", padx=10)

                var = tk.StringVar(value="Present")
                attendance_vars.append((s["student_id"], var))

                ctk.CTkRadioButton(row, text="Present", variable=var, value="Present").pack(side="left", padx=10)
                ctk.CTkRadioButton(row, text="Absent", variable=var, value="Absent").pack(side="left", padx=10)

        ctk.CTkButton(dialog, text="Load Students", command=load_students).pack(pady=5)

        def save():
            course_id = course_map.get(course_menu.get())
            date = date_entry.get_date()

            for sid, var in attendance_vars:
                self.app.db.mark_attendance((sid, course_id, date, var.get(), None))

            messagebox.showinfo("Success", "Attendance saved successfully")
            dialog.destroy()

        ctk.CTkButton(
            dialog,
            text="💾 Save Attendance",
            fg_color=COLORS["success"],
            command=save
        ).pack(pady=15)
