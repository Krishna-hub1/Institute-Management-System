import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import tkinter as tk

from config import COLORS



class AttendanceModule:
    """Feature module extracted from the original application."""

    def show_attendance(self):
            """Display attendance management section"""
            header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=80)
            header.pack(fill="x", padx=30, pady=(20, 10))

            title = ctk.CTkLabel(header, text="📝 Attendance Management", font=ctk.CTkFont(size=28, weight="bold"))
            title.pack(side="left")

            mark_btn = ctk.CTkButton(
                header, text="✅ Mark Attendance", width=160, height=40,
                font=ctk.CTkFont(size=13, weight="bold"), fg_color=COLORS["success"],
                command=self.show_mark_attendance_dialog
            )
            mark_btn.pack(side="right")

            # Filter section
            filter_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
            filter_frame.pack(fill="x", padx=30, pady=10)

            ctk.CTkLabel(filter_frame, text="Date:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
            date_filter = DateEntry(filter_frame, width=15, background=COLORS["primary"],
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            date_filter.pack(side="left", padx=5)

            ctk.CTkLabel(filter_frame, text="Course:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left",
                                                                                                      padx=(20, 5))
            courses = self.db.get_all_courses()
            course_dict = {c['course_name']: c['course_id'] for c in courses}
            course_names = ["All"] + list(course_dict.keys())
            course_filter = ctk.CTkOptionMenu(filter_frame, values=course_names, width=200, height=35)
            course_filter.pack(side="left", padx=5)

            def view_attendance():
                date = date_filter.get_date()
                selected_course = course_filter.get()
                course_id = course_dict.get(selected_course) if selected_course != "All" else None

                records = self.db.get_attendance_by_date(date, course_id)

                # Clear previous info
                for widget in info_frame.winfo_children():
                    widget.destroy()

                title_label = ctk.CTkLabel(
                    info_frame,
                    text=f"📅 Attendance Records - {date}",
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color="white"
                )
                title_label.pack(pady=(10, 20))

                if not records:
                    ctk.CTkLabel(
                        info_frame,
                        text="No attendance records found for this date!",
                        font=ctk.CTkFont(size=16),
                        text_color="white"
                    ).pack(pady=50)
                    return

                # ====== Summary counts ======
                total = len(records)
                present = sum(1 for r in records if r['status'] == "Present")
                absent = total - present

                summary_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                summary_frame.pack(pady=(0, 10))

                ctk.CTkLabel(
                    summary_frame,
                    text=f"🧾 Total: {total}",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="white"
                ).pack(side="left", padx=15)

                ctk.CTkLabel(
                    summary_frame,
                    text=f"✅ Present: {present}",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#00E0FF"  # light cyan for better contrast
                ).pack(side="left", padx=15)

                ctk.CTkLabel(
                    summary_frame,
                    text=f"❌ Absent: {absent}",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color='#F28B82'
                ).pack(side="left", padx=15)

                # ====== Table Container ======
                table_container = ctk.CTkScrollableFrame(info_frame, fg_color="transparent")
                table_container.pack(fill="both", expand=True, padx=30, pady=10)

                # ====== Table Header ======
                headers = ["Student Name", "Course", "Status"]
                column_widths = [300, 250, 150]

                header_frame = ctk.CTkFrame(table_container, fg_color=COLORS["primary"], corner_radius=0)
                header_frame.pack(fill="x")

                for col, header in enumerate(headers):
                    ctk.CTkLabel(
                        header_frame,
                        text=header,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color="white",
                        anchor="center",
                        width=column_widths[col]
                    ).grid(row=0, column=col, padx=1, pady=1, sticky="nsew")

                for i in range(len(headers)):
                    header_frame.grid_columnconfigure(i, weight=1, uniform="col")

                # ====== Data Rows with Grid Lines ======
                grid_color = "#3a3a3a"
                for idx, r in enumerate(records):
                    row_frame = ctk.CTkFrame(table_container, fg_color="transparent", corner_radius=0)
                    row_frame.pack(fill="x", pady=0)

                    bg_color = "#2b2b2b" if idx % 2 == 0 else "#1f1f1f"
                    cells = [
                        f"{r['first_name']} {r['last_name']}",
                        r['course_name'],
                        r['status']
                    ]

                    for col, text in enumerate(cells):
                        fg_color = bg_color
                        text_color = "white"

                        if col == 2:  # status column
                            if text == "Present":
                                fg_color = "#0f5132"  # calm dark green background
                                text_color = "#aaf7ff"  # subtle bright cyan
                            elif text == "Absent":
                                fg_color = COLORS["danger"]

                        label = ctk.CTkLabel(
                            row_frame,
                            text=text,
                            font=ctk.CTkFont(size=13),
                            text_color=text_color,
                            anchor="center",
                            width=column_widths[col],
                            fg_color=fg_color,
                            corner_radius=0
                        )
                        label.grid(row=0, column=col, padx=(0, 1), pady=(0, 1), sticky="nsew")

                        row_frame.grid_columnconfigure(col, weight=1, uniform="col")

                    # horizontal divider line
                    tk.Frame(row_frame, bg=grid_color, height=1).grid(row=1, column=0, columnspan=len(headers), sticky="ew")

            view_btn = ctk.CTkButton(filter_frame, text="View Records", width=140, height=35, command=view_attendance)
            view_btn.pack(side="left", padx=20)

            # Info message
            info_frame = ctk.CTkFrame(self.main_content, fg_color=COLORS["info"], corner_radius=15)
            info_frame.pack(fill="both", expand=True, padx=30, pady=20)

            detail_label=ctk.CTkLabel(
                info_frame,
                text="📊 Attendance Tracking System\n\nUse 'Mark Attendance' to record student presence.\nView records by selecting date and course filters.",
                font=ctk.CTkFont(size=16),
                text_color="white"
            )
            detail_label.pack(expand=True, pady=50)

    def show_mark_attendance_dialog(self):
            """Dialog to mark attendance"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Mark Attendance")
            dialog.geometry("660x600+10+10")
            dialog.transient(self)
            dialog.grab_set()

            ctk.CTkLabel(dialog, text="✅ Mark Attendance", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

            # Course selection
            select_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            select_frame.pack(fill="x", padx=40, pady=10)

            ctk.CTkLabel(select_frame, text="Select Course:", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left",
                                                                                                             padx=10)
            courses = self.db.get_all_courses()
            course_dict = {c['course_name']: c['course_id'] for c in courses}
            course_menu = ctk.CTkOptionMenu(select_frame, values=list(course_dict.keys()), width=300)
            course_menu.pack(side="left", padx=10)

            ctk.CTkLabel(select_frame, text="Date:", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=10)
            date_entry = DateEntry(select_frame, width=15, background=COLORS["primary"],
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            date_entry.pack(side="left", padx=10)

            # Student list
            student_scroll = ctk.CTkScrollableFrame(dialog, height=350)
            student_scroll.pack(fill="both", expand=True, padx=40, pady=10)

            attendance_vars = []

            def load_students():
                for widget in student_scroll.winfo_children():
                    widget.destroy()
                attendance_vars.clear()

                selected_course = course_menu.get()
                course_id = course_dict.get(selected_course)

                students = [s for s in self.db.get_all_students() if s['course_id'] == course_id]

                if not students:
                    ctk.CTkLabel(student_scroll, text="No students in this course").pack(pady=20)
                    return

                for student in students:
                    student_frame = ctk.CTkFrame(student_scroll, fg_color=COLORS["sidebar"], corner_radius=10)
                    student_frame.pack(fill="x", pady=5)

                    name_label = ctk.CTkLabel(
                        student_frame,
                        text=f"{student['first_name']} {student['last_name']} ({student['student_id']})",
                        font=ctk.CTkFont(size=13),
                        width=300,
                        anchor="w"
                    )
                    name_label.pack(side="left", padx=15, pady=10)

                    var = tk.StringVar(value="Present")
                    attendance_vars.append((student['student_id'], var))

                    present_radio = ctk.CTkRadioButton(student_frame, text="Present", variable=var, value="Present")
                    present_radio.pack(side="left", padx=10)

                    absent_radio = ctk.CTkRadioButton(student_frame, text="Absent", variable=var, value="Absent")
                    absent_radio.pack(side="left", padx=10)

            load_btn = ctk.CTkButton(dialog, text="Load Students", width=150, height=35, command=load_students)
            load_btn.pack(pady=5)

            def save_attendance():
                selected_course = course_menu.get()
                course_id = course_dict.get(selected_course)
                date = date_entry.get_date()

                success_count = 0
                for student_id, var in attendance_vars:
                    status = var.get()
                    attendance_data = (student_id, course_id, date, status, None)
                    success, _ = self.db.mark_attendance(attendance_data)
                    if success:
                        success_count += 1

                messagebox.showinfo("Success", f"Attendance marked for {success_count} students!")
                dialog.destroy()

            save_btn = ctk.CTkButton(dialog, text="💾 Save Attendance", width=180, height=45,
                                     fg_color=COLORS["success"], command=save_attendance)
            save_btn.pack(pady=10)
