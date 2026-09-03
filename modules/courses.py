import customtkinter as ctk
from tkinter import messagebox

from config import COLORS



class CoursesModule:
    """Feature module extracted from the original application."""

    def show_courses(self):
            """Display course management section"""
            # Header
            header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=80)
            header.pack(fill="x", padx=30, pady=(20, 10))

            title = ctk.CTkLabel(
                header,
                text="📚 Course Management",
                font=ctk.CTkFont(size=28, weight="bold")
            )
            title.pack(side="left")

            add_btn = ctk.CTkButton(
                header,
                text="➕ Add Course",
                width=140,
                height=40,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLORS["success"],
                command=self.show_add_course_dialog
            )
            add_btn.pack(side="right", padx=5)

            # Courses Grid
            courses_scroll = ctk.CTkScrollableFrame(self.main_content)
            courses_scroll.pack(fill="both", expand=True, padx=30, pady=20)

            courses = self.db.get_all_courses()

            if not courses:
                no_data = ctk.CTkLabel(
                    courses_scroll,
                    text="No courses available. Add your first course!",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data.pack(pady=50)
            else:
                for idx, course in enumerate(courses):
                    course_card = ctk.CTkFrame(courses_scroll, fg_color=COLORS["sidebar"], corner_radius=15)
                    course_card.pack(fill="x", pady=10, padx=10)

                    # Course info
                    info_frame = ctk.CTkFrame(course_card, fg_color="transparent")
                    info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)

                    course_name = ctk.CTkLabel(
                        info_frame,
                        text=course['course_name'],
                        font=ctk.CTkFont(size=18, weight="bold")
                    )
                    course_name.pack(anchor="w")

                    course_code = ctk.CTkLabel(
                        info_frame,
                        text=f"Code: {course['course_code']} | Duration: {course['duration_months']} months | Fees: ₹{course['fees']:.2f}",
                        font=ctk.CTkFont(size=12),
                        text_color="gray"
                    )
                    course_code.pack(anchor="w", pady=5)

                    students_label = ctk.CTkLabel(
                        info_frame,
                        text=f"👨‍🎓 {course['student_count']} students enrolled",
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=COLORS["info"]
                    )
                    students_label.pack(anchor="w", pady=5)

                    # Action buttons
                    btn_frame = ctk.CTkFrame(course_card, fg_color="transparent")
                    btn_frame.pack(side="right", padx=20)

                    edit_btn = ctk.CTkButton(
                        btn_frame,
                        text="✏️ Edit",
                        width=100,
                        height=35,
                        fg_color=COLORS["warning"],
                        command=lambda c=course: self.show_edit_course_dialog(c)
                    )
                    edit_btn.pack(pady=5)

                    delete_btn = ctk.CTkButton(
                        btn_frame,
                        text="🗑️ Delete",
                        width=100,
                        height=35,
                        fg_color=COLORS["danger"],
                        command=lambda c=course: self.delete_course(c)
                    )
                    delete_btn.pack(pady=5)

    def show_add_course_dialog(self):
            """Dialog to add new course"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Add New Course")
            dialog.geometry("500x660+10+10")
            dialog.transient(self)
            dialog.grab_set()

            ctk.CTkLabel(dialog, text="➕ Add New Course", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

            form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            form_frame.pack(fill="both", expand=True, padx=40, pady=20)

            ctk.CTkLabel(form_frame, text="Course Name: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                           anchor="w")
            name_entry = ctk.CTkEntry(form_frame, width=400, height=35, placeholder_text="Enter course name")
            name_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Course Code: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                           anchor="w")
            code_entry = ctk.CTkEntry(form_frame, width=400, height=35, placeholder_text="Enter course code")
            code_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Description:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                         anchor="w")
            desc_entry = ctk.CTkTextbox(form_frame, width=400, height=80)
            desc_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Duration (months):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                               anchor="w")
            duration_entry = ctk.CTkEntry(form_frame, width=400, height=35, placeholder_text="Enter duration in months")
            duration_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Fees (₹):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                      anchor="w")
            fees_entry = ctk.CTkEntry(form_frame, width=400, height=35, placeholder_text="Enter course fees")
            fees_entry.pack(pady=5)

            def save_course():
                if not name_entry.get().strip() or not code_entry.get().strip():
                    messagebox.showwarning("Validation Error", "Course name and code are required!")
                    return

                course_data = (
                    name_entry.get().strip(),
                    code_entry.get().strip(),
                    desc_entry.get("1.0", "end-1c").strip() or None,
                    int(duration_entry.get() or 0),
                    float(fees_entry.get() or 0)
                )

                success, message = self.db.add_course(course_data)
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.navigate_to("Courses")
                else:
                    messagebox.showerror("Error", message)

            save_btn = ctk.CTkButton(dialog, text="💾 Save Course", width=180, height=45,
                                     fg_color=COLORS["success"], command=save_course)
            save_btn.pack(pady=10)

    def show_edit_course_dialog(self, course):
            """Dialog to edit course"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Edit Course")
            dialog.geometry("500x660+10+10")
            dialog.transient(self)
            dialog.grab_set()

            ctk.CTkLabel(dialog, text="✏️ Edit Course", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

            form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            form_frame.pack(fill="both", expand=True, padx=40, pady=20)

            ctk.CTkLabel(form_frame, text="Course Name: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                           anchor="w")
            name_entry = ctk.CTkEntry(form_frame, width=400, height=35)
            name_entry.insert(0, course['course_name'])
            name_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Course Code: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                           anchor="w")
            code_entry = ctk.CTkEntry(form_frame, width=400, height=35)
            code_entry.insert(0, course['course_code'])
            code_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Description:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                         anchor="w")
            desc_entry = ctk.CTkTextbox(form_frame, width=400, height=80)
            if course['description']:
                desc_entry.insert("1.0", course['description'])
            desc_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Duration (months):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                               anchor="w")
            duration_entry = ctk.CTkEntry(form_frame, width=400, height=35)
            duration_entry.insert(0, str(course['duration_months'] or 0))
            duration_entry.pack(pady=5)

            ctk.CTkLabel(form_frame, text="Fees (₹):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                      anchor="w")
            fees_entry = ctk.CTkEntry(form_frame, width=400, height=35)
            fees_entry.insert(0, str(course['fees'] or 0))
            fees_entry.pack(pady=5)

            def update_course():
                course_data = (
                    name_entry.get().strip(),
                    code_entry.get().strip(),
                    desc_entry.get("1.0", "end-1c").strip() or None,
                    int(duration_entry.get() or 0),
                    float(fees_entry.get() or 0)
                )

                success, message = self.db.update_course(course['course_id'], course_data)
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.navigate_to("Courses")
                else:
                    messagebox.showerror("Error", message)

            update_btn = ctk.CTkButton(dialog, text="💾 Update Course", width=180, height=45,
                                       fg_color=COLORS["warning"], command=update_course)
            update_btn.pack(pady=10)

    def delete_course(self, course):
            """Delete course"""
            if messagebox.askyesno("Confirm Delete",
                                   f"Delete course '{course['course_name']}'?\nThis will affect {course['student_count']} students!"):
                success, message = self.db.delete_course(course['course_id'])
                if success:
                    messagebox.showinfo("Success", message)
                    self.navigate_to("Courses")
                else:
                    messagebox.showerror("Error", message)
