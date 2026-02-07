import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk
import os
import shutil
from utils import sort_students_by_name, binary_search_student_by_id
from config import COLORS


class StudentsModule:
    def __init__(self, app):
        self.app = app
        self.selected_photo_path = None
        self.photo_preview_label = None
        self.student_tree = None

    # ================= MAIN VIEW =================

    def show(self):
        for w in self.app.main_content.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self.app.main_content, fg_color="transparent", height=80)
        header.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="👨‍🎓 Institute Student Management",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(side="left")

        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")

        ctk.CTkButton(
            btn_frame,
            text="➕ Add Student",
            fg_color=COLORS["success"],
            command=self.show_add_student_dialog
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            fg_color=COLORS["info"],
            command=self.load_students
        ).pack(side="left", padx=5)

        self._create_table()
        self.load_students()

    # ================= TABLE =================

    def _create_table(self):
        table_frame = ctk.CTkFrame(self.app.main_content)
        table_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tree_scroll = tk.Scrollbar(table_frame)
        tree_scroll.pack(side="right", fill="y")

        columns = ("ID", "Name", "Gender", "Email", "Course", "Status")

        self.student_tree = tk.ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll.set
        )

        tree_scroll.config(command=self.student_tree.yview)

        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=140)

        self.student_tree.pack(fill="both", expand=True)

        self.student_tree.bind("<Double-1>", lambda e: self.view_student())

    # ================= DATA =================

    def load_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)

        students = self.app.db.get_all_students()

        for s in students:
            name = f"{s['first_name']} {s['last_name']}"
            self.student_tree.insert(
                "",
                "end",
                values=(
                    s["student_id"],
                    name,
                    s["gender"],
                    s["email"],
                    s.get("course_name", "N/A"),
                    s["status"]
                )
            )

    # ================= ADD STUDENT =================

    def show_add_student_dialog(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Add Student")
        dialog.geometry("800x600")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Add New Student",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        form = ctk.CTkFrame(dialog)
        form.pack(fill="both", expand=True, padx=30, pady=10)

        first_name = ctk.CTkEntry(form, placeholder_text="First Name")
        last_name = ctk.CTkEntry(form, placeholder_text="Last Name")
        gender = ctk.CTkOptionMenu(form, values=["Male", "Female", "Other"])

        first_name.pack(pady=8)
        last_name.pack(pady=8)
        gender.pack(pady=8)

        def save():
            if not first_name.get() or not last_name.get():
                messagebox.showwarning("Error", "Name required")
                return

            student_id = self.app.db.generate_student_id()
            data = (
                student_id,
                first_name.get(),
                last_name.get(),
                gender.get(),
                None, None, None, None,
                None,
                datetime.now().date(),
                None,
                "Active"
            )

            success, msg = self.app.db.add_student(data)
            if success:
                messagebox.showinfo("Success", msg)
                dialog.destroy()
                self.load_students()
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(dialog, text="Save", fg_color=COLORS["success"], command=save).pack(pady=20)

    # ================= VIEW =================

    def view_student(self):
        selected = self.student_tree.selection()
        if not selected:
            return

        student_id = self.student_tree.item(selected[0])["values"][0]
        student = self.app.db.get_student_by_id(student_id)

        messagebox.showinfo(
            "Student Profile",
            f"{student['first_name']} {student['last_name']}\n"
            f"Course: {student.get('course_name', 'N/A')}\n"
            f"Status: {student['status']}"
        )
