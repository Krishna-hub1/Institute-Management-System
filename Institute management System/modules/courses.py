import customtkinter as ctk
from tkinter import messagebox

from config import COLORS


class CoursesModule:
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
            text="📚 Course Management",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="➕ Add Course",
            fg_color=COLORS["success"],
            command=self.show_add_course_dialog
        ).pack(side="right")

        self._course_list()

    # ================= LIST =================

    def _course_list(self):
        scroll = ctk.CTkScrollableFrame(self.app.main_content)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)

        courses = self.app.db.get_all_courses()

        if not courses:
            ctk.CTkLabel(
                scroll,
                text="No courses available. Add your first course!",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            ).pack(pady=50)
            return

        for course in courses:
            card = ctk.CTkFrame(scroll, fg_color=COLORS["sidebar"], corner_radius=15)
            card.pack(fill="x", pady=10, padx=10)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=20, pady=15)

            ctk.CTkLabel(
                info,
                text=course["course_name"],
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"Code: {course['course_code']} | "
                     f"Duration: {course['duration_months']} months | "
                     f"Fees: ₹{course['fees']}",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="w", pady=5)

            ctk.CTkLabel(
                info,
                text=f"👨‍🎓 {course['student_count']} students enrolled",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS["info"]
            ).pack(anchor="w", pady=5)

            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(side="right", padx=20)

            ctk.CTkButton(
                btns,
                text="✏️ Edit",
                width=100,
                fg_color=COLORS["warning"],
                command=lambda c=course: self.show_edit_course_dialog(c)
            ).pack(pady=5)

            ctk.CTkButton(
                btns,
                text="🗑️ Delete",
                width=100,
                fg_color=COLORS["danger"],
                command=lambda c=course: self.delete_course(c)
            ).pack(pady=5)

    # ================= ADD =================

    def show_add_course_dialog(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Add Course")
        dialog.geometry("500x600")
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="➕ Add New Course",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)

        form = ctk.CTkFrame(dialog)
        form.pack(fill="both", expand=True, padx=40, pady=20)

        name = ctk.CTkEntry(form, placeholder_text="Course Name")
        code = ctk.CTkEntry(form, placeholder_text="Course Code")
        desc = ctk.CTkTextbox(form, height=80)
        duration = ctk.CTkEntry(form, placeholder_text="Duration (months)")
        fees = ctk.CTkEntry(form, placeholder_text="Fees")

        for w in (name, code, desc, duration, fees):
            w.pack(pady=8)

        def save():
            if not name.get().strip() or not code.get().strip():
                messagebox.showwarning("Validation Error", "Name and code required")
                return

            data = (
                name.get().strip(),
                code.get().strip(),
                desc.get("1.0", "end-1c") or None,
                int(duration.get() or 0),
                float(fees.get() or 0)
            )

            success, msg = self.app.db.add_course(data)
            if success:
                messagebox.showinfo("Success", msg)
                dialog.destroy()
                self.show()
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(
            dialog,
            text="💾 Save Course",
            fg_color=COLORS["success"],
            command=save
        ).pack(pady=15)

    # ================= EDIT =================

    def show_edit_course_dialog(self, course):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Edit Course")
        dialog.geometry("500x600")
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="✏️ Edit Course",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)

        form = ctk.CTkFrame(dialog)
        form.pack(fill="both", expand=True, padx=40, pady=20)

        name = ctk.CTkEntry(form)
        code = ctk.CTkEntry(form)
        desc = ctk.CTkTextbox(form, height=80)
        duration = ctk.CTkEntry(form)
        fees = ctk.CTkEntry(form)

        name.insert(0, course["course_name"])
        code.insert(0, course["course_code"])
        if course["description"]:
            desc.insert("1.0", course["description"])
        duration.insert(0, course["duration_months"])
        fees.insert(0, course["fees"])

        for w in (name, code, desc, duration, fees):
            w.pack(pady=8)

        def update():
            data = (
                name.get().strip(),
                code.get().strip(),
                desc.get("1.0", "end-1c") or None,
                int(duration.get() or 0),
                float(fees.get() or 0)
            )

            success, msg = self.app.db.update_course(course["course_id"], data)
            if success:
                messagebox.showinfo("Success", msg)
                dialog.destroy()
                self.show()
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(
            dialog,
            text="💾 Update Course",
            fg_color=COLORS["warning"],
            command=update
        ).pack(pady=15)

    # ================= DELETE =================

    def delete_course(self, course):
        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete course '{course['course_name']}'?\n"
            f"This affects {course['student_count']} students."
        ):
            success, msg = self.app.db.delete_course(course["course_id"])
            if success:
                messagebox.showinfo("Success", msg)
                self.show()
            else:
                messagebox.showerror("Error", msg)
