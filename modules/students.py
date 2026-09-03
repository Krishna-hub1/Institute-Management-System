import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import os
import shutil
from config import COLORS
class StudentsModule:
    """Feature module extracted from the original application."""

    def show_students(self):
            """Display student management section"""
            # Header
            header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=80)
            header.pack(fill="x", padx=30, pady=(20, 10))

            title = ctk.CTkLabel(
                header,
                text="👨‍🎓 Institute Student Management",
                font=ctk.CTkFont(size=28, weight="bold")
            )
            title.pack(side="left")

            # Action buttons
            btn_frame = ctk.CTkFrame(header, fg_color="transparent")
            btn_frame.pack(side="right")

            add_btn = ctk.CTkButton(
                btn_frame,
                text="➕ Add Student",
                width=140,
                height=40,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLORS["success"],
                command=self.show_add_student_dialog
            )
            add_btn.pack(side="left", padx=5)

            refresh_btn = ctk.CTkButton(
                btn_frame,
                text="🔄 Refresh",
                width=120,
                height=40,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLORS["info"],
                command=lambda: self.navigate_to("Students")
            )
            refresh_btn.pack(side="left", padx=5)

            export_btn = ctk.CTkButton(
                btn_frame,
                text="📥 Export Excel",
                width=140,
                height=40,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLORS["warning"],
                command=self.export_filtered_students_to_excel
            )
            export_btn.pack(side="left", padx=5)

            # Search and Filter Section
            search_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
            search_frame.pack(fill="x", padx=30, pady=10)

            self.student_search_entry = ctk.CTkEntry(
                search_frame,
                placeholder_text="🔍 Search by ID, Name, Email...",
                width=300,
                height=40,
                font=ctk.CTkFont(size=13)
            )
            self.student_search_entry.pack(side="left", padx=(0, 10))

            search_btn = ctk.CTkButton(
                search_frame,
                text="Search",
                width=100,
                height=40,
                command=self.search_students
            )
            search_btn.pack(side="left", padx=5)

            # Filter dropdowns
            ctk.CTkLabel(search_frame, text="Course:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(20, 5))
            courses = self.db.get_all_courses()
            course_names = ["All"] + [c['course_name'] for c in courses]
            self.student_course_filter = ctk.CTkOptionMenu(search_frame, values=course_names, width=150, height=40)
            self.student_course_filter.pack(side="left", padx=5)

            ctk.CTkLabel(search_frame, text="Gender:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(10, 5))
            self.student_gender_filter = ctk.CTkOptionMenu(search_frame, values=["All", "Male", "Female", "Other"],
                                                           width=120, height=40)
            self.student_gender_filter.pack(side="left", padx=5)

            filter_btn = ctk.CTkButton(
                search_frame,
                text="Apply Filters",
                width=120,
                height=40,
                command=self.filter_students
            )
            filter_btn.pack(side="left", padx=10)

            # Treeview Table
            table_frame = ctk.CTkFrame(self.main_content)
            table_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

            # Create Treeview with ttk
            import tkinter.ttk as ttk

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", background="#2b2b2b", foreground="white",
                            fieldbackground="#2b2b2b", font=('Arial', 10))
            style.configure("Treeview.Heading", background=COLORS["primary"],
                            foreground="white", font=('Arial', 11, 'bold'))
            style.map('Treeview', background=[('selected', COLORS["success"])])

            # Scrollbars
            tree_scroll_y = tk.Scrollbar(table_frame, orient="vertical")
            tree_scroll_y.pack(side="right", fill="y")

            tree_scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
            tree_scroll_x.pack(side="bottom", fill="x")

            # Treeview
            columns = ("ID", "Name", "Gender", "DOB", "Email", "Phone", "Course", "Admission", "Status")
            self.student_tree = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings",
                yscrollcommand=tree_scroll_y.set,
                xscrollcommand=tree_scroll_x.set,
                height=15
            )

            tree_scroll_y.config(command=self.student_tree.yview)
            tree_scroll_x.config(command=self.student_tree.xview)

            # Define headings and columns
            col_widths = [120, 180, 80, 100, 180, 120, 150, 100, 80]
            for col, width in zip(columns, col_widths):
                self.student_tree.heading(col, text=col, anchor="w")
                self.student_tree.column(col, width=width, anchor="w")

            self.student_tree.pack(fill="both", expand=True, padx=10, pady=10)

            # Alternate row colors
            self.student_tree.tag_configure('oddrow', background='#1e1e1e')
            self.student_tree.tag_configure('evenrow', background='#2b2b2b')

            # Right-click menu
            self.student_tree_menu = tk.Menu(self.student_tree, tearoff=0, bg='#2b2b2b', fg='white')
            self.student_tree_menu.add_command(label="✏️ Edit", command=self.edit_selected_student)
            self.student_tree_menu.add_command(label="👁️ View Profile", command=self.view_student_profile)
            self.student_tree_menu.add_command(label="📋 Copy ID", command=self.copy_student_id)
            self.student_tree_menu.add_separator()
            self.student_tree_menu.add_command(label="🗑️ Delete", command=self.delete_selected_student)

            self.student_tree.bind("<Button-3>", self.show_student_context_menu)
            self.student_tree.bind("<Double-1>", lambda e: self.view_student_profile())

            # Load data
            self.load_students_data()

    def load_students_data(self, students=None):
            """Load students into treeview"""
            # Clear existing data
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)

            # Get students
            if students is None:
                students = self.db.get_all_students()

            # Insert data
            for idx, student in enumerate(students):
                name = f"{student['first_name']} {student['last_name']}"
                values = (
                    student['student_id'],
                    name,
                    student['gender'],
                    student['dob'].strftime('%Y-%m-%d') if student['dob'] else '',
                    student['email'],
                    student['phone'],
                    student['course_name'] if student.get('course_name') else 'N/A',
                    student['admission_date'].strftime('%Y-%m-%d') if student['admission_date'] else '',
                    student['status']
                )

                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.student_tree.insert('', 'end', values=values, tags=(tag,))

    def search_students(self):
            """Search students"""
            search_term = self.student_search_entry.get().strip()
            if search_term:
                students = self.db.search_students(search_term)
                self.load_students_data(students)
            else:
                self.load_students_data()

    def filter_students(self):
            """Filter students by course and gender"""
            # Get all students first
            students = self.db.get_all_students()

            course_filter = self.student_course_filter.get()
            gender_filter = self.student_gender_filter.get()

            filtered = students

            if course_filter != "All":
                filtered = [s for s in filtered if s.get('course_name') == course_filter]

            if gender_filter != "All":
                filtered = [s for s in filtered if s['gender'] == gender_filter]

            self.load_students_data(filtered)

    def show_student_context_menu(self, event):
            """Show right-click context menu"""
            try:
                self.student_tree.selection_set(self.student_tree.identify_row(event.y))
                self.student_tree_menu.post(event.x_root, event.y_root)
            except:
                pass

    def copy_student_id(self):
            """Copy student ID to clipboard"""
            selected = self.student_tree.selection()
            if selected:
                item = self.student_tree.item(selected[0])
                student_id = item['values'][0]
                self.clipboard_clear()
                self.clipboard_append(student_id)
                messagebox.showinfo("Copied", f"Student ID {student_id} copied to clipboard!")

    def delete_selected_student(self):
            """Delete selected student"""
            selected = self.student_tree.selection()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select a student to delete!")
                return

            item = self.student_tree.item(selected[0])
            student_id = item['values'][0]
            student_name = item['values'][1]

            if messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete {student_name}?\nThis action cannot be undone!"):
                success, message = self.db.delete_student(student_id)
                if success:
                    messagebox.showinfo("Success", message)
                    self.load_students_data()
                    # Refresh dashboard
                    if self.current_section == "Dashboard":
                        self.show_dashboard()
                else:
                    messagebox.showerror("Error", message)

    def edit_selected_student(self):
            """Edit selected student"""
            selected = self.student_tree.selection()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select a student to edit!")
                return

            item = self.student_tree.item(selected[0])
            student_id = item['values'][0]

            student = self.db.get_student_by_id(student_id)
            if student:
                self.show_edit_student_dialog(student)

    def view_student_profile(self):
            """View detailed student profile"""
            selected = self.student_tree.selection()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select a student to view!")
                return

            item = self.student_tree.item(selected[0])
            student_id = item['values'][0]

            student = self.db.get_student_by_id(student_id)
            if student:
                self.show_student_profile_dialog(student)

    def show_add_student_dialog(self):
            """Show dialog to add new student"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Add New Student")
            dialog.geometry("900x680+10+0")
            dialog.transient(self)
            dialog.grab_set()

            # Make dialog responsive
            dialog.grid_columnconfigure(0, weight=1)
            dialog.grid_rowconfigure(1, weight=1)

            # Header
            header = ctk.CTkFrame(dialog, fg_color=COLORS["success"], height=60)
            header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

            ctk.CTkLabel(
                header,
                text="➕ Add New Student",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="white"
            ).pack(pady=15)

            # Scrollable form
            form_scroll = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
            form_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

            # Left side: Form fields
            left_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
            left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

            # Auto-generate Student ID
            student_id = self.db.generate_student_id()

            # Student ID (Read-only)
            ctk.CTkLabel(left_frame, text="Student ID:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                        anchor="w")
            id_entry = ctk.CTkEntry(left_frame, width=400, height=35)
            id_entry.insert(0, student_id)
            id_entry.configure(state="readonly")
            id_entry.pack(pady=5)

            # First Name
            ctk.CTkLabel(left_frame, text="First Name: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                          anchor="w")
            first_name_entry = ctk.CTkEntry(left_frame, width=400, height=35, placeholder_text="Enter first name")
            first_name_entry.pack(pady=5)

            # Last Name
            ctk.CTkLabel(left_frame, text="Last Name: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                         anchor="w")
            last_name_entry = ctk.CTkEntry(left_frame, width=400, height=35, placeholder_text="Enter last name")
            last_name_entry.pack(pady=5)

            # Gender
            ctk.CTkLabel(left_frame, text="Gender: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                      anchor="w")
            gender_menu = ctk.CTkOptionMenu(left_frame, width=400, height=35, values=["Male", "Female", "Other"])
            gender_menu.pack(pady=5)

            # Date of Birth
            ctk.CTkLabel(left_frame, text="Date of Birth: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                             anchor="w")
            dob_entry = DateEntry(
                left_frame,
                width=52,  # reduces text clipping and fits same width as CTkEntry
                background=COLORS["primary"],
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                font=("Arial", 14),  # increases font size (affects height)
            )
            dob_entry.pack(pady=5, ipady=10)  # ipady adds vertical padding inside


            # Email
            ctk.CTkLabel(left_frame, text="Email:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w")
            email_entry = ctk.CTkEntry(left_frame, width=400, height=35, placeholder_text="Enter email")
            email_entry.pack(pady=5)

            # Phone
            ctk.CTkLabel(left_frame, text="Phone:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w")
            phone_entry = ctk.CTkEntry(left_frame, width=400, height=35, placeholder_text="Enter phone number")
            phone_entry.pack(pady=5)

            # Address
            ctk.CTkLabel(left_frame, text="Address:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                     anchor="w")
            address_entry = ctk.CTkTextbox(left_frame, width=400, height=80)
            address_entry.pack(pady=5)

            # Course
            ctk.CTkLabel(left_frame, text="Course: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                      anchor="w")
            courses = self.db.get_all_courses()
            course_dict = {c['course_name']: c['course_id'] for c in courses}
            course_names = list(course_dict.keys()) if courses else ["No courses available"]
            course_menu = ctk.CTkOptionMenu(left_frame, width=400, height=35, values=course_names)
            course_menu.pack(pady=5)

            # Admission Date
            ctk.CTkLabel(left_frame, text="Admission Date: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                              anchor="w")
            admission_entry = DateEntry(
                left_frame,
                width=52,
                background=COLORS["primary"],
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                font=("Arial", 14),
            )
            admission_entry.pack(pady=5, ipady=10)

            # Status
            ctk.CTkLabel(left_frame, text="Status:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                    anchor="w")
            status_menu = ctk.CTkOptionMenu(left_frame, width=400, height=35, values=["Active", "Inactive", "Graduated"])
            status_menu.set("Active")
            status_menu.pack(pady=5)

            # Right side: Photo upload
            right_frame = ctk.CTkFrame(form_scroll, fg_color=COLORS["sidebar"], corner_radius=15)
            right_frame.pack(side="right", fill="y", padx=(20, 0))

            ctk.CTkLabel(right_frame, text="Student Photo",
                         font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)

            # Photo preview
            photo_frame = ctk.CTkFrame(right_frame, width=250, height=250, fg_color="gray20")
            photo_frame.pack(pady=10, padx=20)
            photo_frame.pack_propagate(False)

            self.selected_photo_path = None
            self.photo_preview_label = ctk.CTkLabel(photo_frame, text="No photo selected\n\n📷",
                                                    font=ctk.CTkFont(size=16), text_color="gray")
            self.photo_preview_label.pack(expand=True)

            # Upload button
            upload_btn = ctk.CTkButton(
                right_frame,
                text="📤 Upload Photo",
                width=200,
                height=40,
                fg_color=COLORS["info"],
                command=lambda: self.upload_photo(self.photo_preview_label)
            )
            upload_btn.pack(pady=10)

            # Clear photo button
            clear_photo_btn = ctk.CTkButton(
                right_frame,
                text="🗑️ Clear Photo",
                width=200,
                height=35,
                fg_color=COLORS["danger"],
                command=lambda: self.clear_photo(self.photo_preview_label)
            )
            clear_photo_btn.pack(pady=5)

            # Buttons
            button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            button_frame.grid(row=2, column=0, pady=20)

            def save_student():
                # Validation
                if not first_name_entry.get().strip():
                    messagebox.showwarning("Validation Error", "First name is required!")
                    return
                if not last_name_entry.get().strip():
                    messagebox.showwarning("Validation Error", "Last name is required!")
                    return
                if not course_names or course_names[0] == "No courses available":
                    messagebox.showwarning("Error", "Please add courses first!")
                    return

                # If photo not uploaded, confirm with user
                if not self.selected_photo_path:
                    confirm = messagebox.askyesno(
                        "No Photo Added",
                        "You haven’t uploaded a student photo.\n\nDo you want to add the student without a photo?"
                    )
                    if not confirm:
                        return  # user cancelled

                # Get course_id
                selected_course = course_menu.get()
                course_id = course_dict.get(selected_course)

                # Prepare data
                student_data = (
                    student_id,
                    first_name_entry.get().strip(),
                    last_name_entry.get().strip(),
                    gender_menu.get(),
                    dob_entry.get_date(),
                    email_entry.get().strip() or None,
                    phone_entry.get().strip() or None,
                    address_entry.get("1.0", "end-1c").strip() or None,
                    course_id,
                    admission_entry.get_date(),
                    self.selected_photo_path,
                    status_menu.get()
                )

                # Add to database
                success, message = self.db.add_student(student_data)

                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.load_students_data()
                else:
                    messagebox.showerror("Error", message)

            save_btn = ctk.CTkButton(
                button_frame,
                text="💾 Save Student",
                width=180,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["success"],
                command=save_student
            )
            save_btn.pack(side="left", padx=10)

            cancel_btn = ctk.CTkButton(
                button_frame,
                text="❌ Cancel",
                width=180,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["danger"],
                command=dialog.destroy
            )
            cancel_btn.pack(side="left", padx=10)

    def upload_photo(self, preview_label):
            """Upload and preview photo"""
            file_path = filedialog.askopenfilename(
                title="Select Student Photo",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
            )

            if file_path:
                try:
                    # Copy to assets/photos
                    filename = os.path.basename(file_path)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_filename = f"{timestamp}_{filename}"
                    dest_path = os.path.join("assets/photos", new_filename)

                    shutil.copy(file_path, dest_path)
                    self.selected_photo_path = dest_path

                    # Show preview
                    img = Image.open(file_path)
                    img = img.resize((230, 230), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)

                    preview_label.configure(image=photo, text="")
                    preview_label.image = photo  # Keep reference

                    messagebox.showinfo("Success", "Photo uploaded successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to upload photo: {str(e)}")

    def clear_photo(self, preview_label):
            """Clear photo selection"""
            self.selected_photo_path = None
            preview_label.configure(image=None, text="No photo selected\n\n📷")
            preview_label.image = None

    def show_edit_student_dialog(self, student):
            """Show dialog to edit student - similar to add but pre-filled"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Edit Student")
            dialog.geometry("900x680+10+0")
            dialog.transient(self)
            dialog.grab_set()

            dialog.grid_columnconfigure(0, weight=1)
            dialog.grid_rowconfigure(1, weight=1)

            # Header
            header = ctk.CTkFrame(dialog, fg_color=COLORS["warning"], height=60)
            header.grid(row=0, column=0, sticky="ew")

            ctk.CTkLabel(
                header,
                text=f"✏️ Edit Student: {student['first_name']} {student['last_name']}",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="white"
            ).pack(pady=15)

            # Scrollable form
            form_scroll = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
            form_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

            # Left side: Form fields
            left_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
            left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

            # Student ID (Read-only)
            ctk.CTkLabel(left_frame, text="Student ID:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                        anchor="w")
            id_entry = ctk.CTkEntry(left_frame, width=400, height=35)
            id_entry.insert(0, student['student_id'])
            id_entry.configure(state="readonly")
            id_entry.pack(pady=5)

            # Pre-fill all fields
            ctk.CTkLabel(left_frame, text="First Name: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                          anchor="w")
            first_name_entry = ctk.CTkEntry(left_frame, width=400, height=35)
            first_name_entry.insert(0, student['first_name'])
            first_name_entry.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Last Name: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                         anchor="w")
            last_name_entry = ctk.CTkEntry(left_frame, width=400, height=35)
            last_name_entry.insert(0, student['last_name'])
            last_name_entry.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Gender: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                      anchor="w")
            gender_menu = ctk.CTkOptionMenu(left_frame, width=400, height=35, values=["Male", "Female", "Other"])
            gender_menu.set(student['gender'])
            gender_menu.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Date of Birth: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                             anchor="w")
            dob_entry = DateEntry(left_frame, width=57, background=COLORS["primary"],
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                  year=student['dob'].year, month=student['dob'].month, day=student['dob'].day)
            dob_entry.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Email:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w")
            email_entry = ctk.CTkEntry(left_frame, width=400, height=35)
            if student['email']:
                email_entry.insert(0, student['email'])
            email_entry.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Phone:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w")
            phone_entry = ctk.CTkEntry(left_frame, width=400, height=35)
            if student['phone']:
                phone_entry.insert(0, student['phone'])
            phone_entry.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Address:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                     anchor="w")
            address_entry = ctk.CTkTextbox(left_frame, width=400, height=80)
            if student['address']:
                address_entry.insert("1.0", student['address'])
            address_entry.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Course: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                      anchor="w")
            courses = self.db.get_all_courses()
            course_dict = {c['course_name']: c['course_id'] for c in courses}
            course_names = list(course_dict.keys())
            course_menu = ctk.CTkOptionMenu(left_frame, width=400, height=35, values=course_names)
            if student.get('course_name'):
                course_menu.set(student['course_name'])
            course_menu.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Admission Date: *", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                              anchor="w")
            admission_entry = DateEntry(left_frame, width=57, background=COLORS["primary"],
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                        year=student['admission_date'].year,
                                        month=student['admission_date'].month,
                                        day=student['admission_date'].day)
            admission_entry.pack(pady=5)

            ctk.CTkLabel(left_frame, text="Status:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5),
                                                                                                    anchor="w")
            status_menu = ctk.CTkOptionMenu(left_frame, width=400, height=35, values=["Active", "Inactive", "Graduated"])
            status_menu.set(student['status'])
            status_menu.pack(pady=5)

            # Right side: Photo
            right_frame = ctk.CTkFrame(form_scroll, fg_color=COLORS["sidebar"], corner_radius=15)
            right_frame.pack(side="right", fill="y", padx=(20, 0))

            ctk.CTkLabel(right_frame, text="Student Photo",
                         font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)

            photo_frame = ctk.CTkFrame(right_frame, width=250, height=250, fg_color="gray20")
            photo_frame.pack(pady=10, padx=20)
            photo_frame.pack_propagate(False)

            self.selected_photo_path = student['photo_path']
            self.photo_preview_label = ctk.CTkLabel(photo_frame, text="", font=ctk.CTkFont(size=16))
            self.photo_preview_label.pack(expand=True)

            # Load existing photo
            if student['photo_path'] and os.path.exists(student['photo_path']):
                try:
                    img = Image.open(student['photo_path'])
                    img = img.resize((230, 230), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.photo_preview_label.configure(image=photo)
                    self.photo_preview_label.image = photo
                except:
                    self.photo_preview_label.configure(text="No photo\n\n📷", text_color="gray")
            else:
                self.photo_preview_label.configure(text="No photo\n\n📷", text_color="gray")

            upload_btn = ctk.CTkButton(
                right_frame,
                text="📤 Upload Photo",
                width=200,
                height=40,
                fg_color=COLORS["info"],
                command=lambda: self.upload_photo(self.photo_preview_label)
            )
            upload_btn.pack(pady=10)

            clear_photo_btn = ctk.CTkButton(
                right_frame,
                text="🗑️ Clear Photo",
                width=200,
                height=35,
                fg_color=COLORS["danger"],
                command=lambda: self.clear_photo(self.photo_preview_label)
            )
            clear_photo_btn.pack(pady=5)

            # Buttons
            button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            button_frame.grid(row=2, column=0, pady=20)

            def update_student():
                selected_course = course_menu.get()
                course_id = course_dict.get(selected_course)

                student_data = (
                    first_name_entry.get().strip(),
                    last_name_entry.get().strip(),
                    gender_menu.get(),
                    dob_entry.get_date(),
                    email_entry.get().strip() or None,
                    phone_entry.get().strip() or None,
                    address_entry.get("1.0", "end-1c").strip() or None,
                    course_id,
                    admission_entry.get_date(),
                    self.selected_photo_path,
                    status_menu.get()
                )

                success, message = self.db.update_student(student['student_id'], student_data)

                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.load_students_data()
                else:
                    messagebox.showerror("Error", message)

            save_btn = ctk.CTkButton(
                button_frame,
                text="💾 Update Student",
                width=180,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["warning"],
                command=update_student
            )
            save_btn.pack(side="left", padx=10)

            cancel_btn = ctk.CTkButton(
                button_frame,
                text="❌ Cancel",
                width=180,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["danger"],
                command=dialog.destroy
            )
            cancel_btn.pack(side="left", padx=10)

    def show_student_profile_dialog(self, student):
            """Show detailed student profile with photo"""
            dialog = ctk.CTkToplevel(self)
            dialog.title(f"Student Profile - {student['first_name']} {student['last_name']}")
            dialog.geometry("700x600+10+10")
            dialog.transient(self)
            dialog.grab_set()

            # Header with photo
            header = ctk.CTkFrame(dialog, fg_color=COLORS["primary"], height=200)
            header.pack(fill="x")

            # Photo
            photo_label = ctk.CTkLabel(header, text="", width=150, height=150)
            photo_label.pack(side="left", padx=30, pady=25)

            if student['photo_path'] and os.path.exists(student['photo_path']):
                try:
                    img = Image.open(student['photo_path'])
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    photo_label.configure(image=photo)
                    photo_label.image = photo
                except:
                    photo_label.configure(text="📷\nNo Photo", font=ctk.CTkFont(size=14))
            else:
                photo_label.configure(text="📷\nNo Photo", font=ctk.CTkFont(size=14))

            # Student info in header
            info_frame = ctk.CTkFrame(header, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, pady=25, padx=20)

            name_label = ctk.CTkLabel(
                info_frame,
                text=f"{student['first_name']} {student['last_name']}",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="white"
            )
            name_label.pack(anchor="w")

            id_label = ctk.CTkLabel(
                info_frame,
                text=f"ID: {student['student_id']}",
                font=ctk.CTkFont(size=14),
                text_color="lightgray"
            )
            id_label.pack(anchor="w", pady=5)

            status_label = ctk.CTkLabel(
                info_frame,
                text=f"Status: {student['status']}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="lightgreen" if student['status'] == "Active" else "orange"
            )
            status_label.pack(anchor="w")

            # Details section
            details_scroll = ctk.CTkScrollableFrame(dialog)
            details_scroll.pack(fill="both", expand=True, padx=20, pady=20)

            # Create detail rows
            details = [
                ("👤 Gender", student['gender']),
                ("🎂 Date of Birth", student['dob'].strftime('%Y-%m-%d') if student['dob'] else 'N/A'),
                ("📧 Email", student['email'] or 'N/A'),
                ("📱 Phone", student['phone'] or 'N/A'),
                ("🏠 Address", student['address'] or 'N/A'),
                ("📚 Course", student.get('course_name') or 'N/A'),
                ("📅 Admission Date",
                 student['admission_date'].strftime('%Y-%m-%d') if student['admission_date'] else 'N/A'),
            ]

            for label, value in details:
                row_frame = ctk.CTkFrame(details_scroll, fg_color=COLORS["sidebar"], corner_radius=10)
                row_frame.pack(fill="x", pady=5)

                ctk.CTkLabel(
                    row_frame,
                    text=label,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    width=180,
                    anchor="w"
                ).pack(side="left", padx=15, pady=12)

                ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    font=ctk.CTkFont(size=13),
                    anchor="w"
                ).pack(side="left", padx=10, pady=12, fill="x", expand=True)

            # Attendance info
            attendance_pct = self.db.get_student_attendance(student['student_id'])
            att_frame = ctk.CTkFrame(details_scroll,
                                     fg_color=COLORS["success"] if attendance_pct >= 75 else COLORS["danger"],
                                     corner_radius=10)
            att_frame.pack(fill="x", pady=10)

            ctk.CTkLabel(
                att_frame,
                text=f"📊 Attendance Rate: {attendance_pct:.1f}%",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="white"
            ).pack(pady=15)

            # Close button
            close_btn = ctk.CTkButton(
                dialog,
                text="Close",
                width=150,
                height=40,
                command=dialog.destroy
            )
            close_btn.pack(pady=15)
