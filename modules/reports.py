import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

from config import COLORS



class ReportsModule:
    """Feature module extracted from the original application."""

    def show_reports(self):
            """Display reports section"""
            header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=80)
            header.pack(fill="x", padx=30, pady=(20, 10))

            title = ctk.CTkLabel(header, text="📈 Reports & Export", font=ctk.CTkFont(size=28, weight="bold"))
            title.pack(side="left")

            # Export options
            export_frame = ctk.CTkFrame(self.main_content)
            export_frame.pack(fill="both", expand=True, padx=30, pady=20)

            ctk.CTkLabel(
                export_frame,
                text="📊 Export Data to Excel",
                font=ctk.CTkFont(size=22, weight="bold")
            ).pack(pady=30)

            # Export buttons
            btn_frame = ctk.CTkFrame(export_frame, fg_color="transparent")
            btn_frame.pack(pady=20)

            students_btn = ctk.CTkButton(
                btn_frame,
                text="📥 Export Students",
                width=200,
                height=60,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["info"],
                command=self.export_students_to_excel
            )
            students_btn.pack(pady=10)

            courses_btn = ctk.CTkButton(
                btn_frame,
                text="📥 Export Courses",
                width=200,
                height=60,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["success"],
                command=self.export_courses_to_excel
            )
            courses_btn.pack(pady=10)

            attendance_btn = ctk.CTkButton(
                btn_frame,
                text="📥 Export Attendance",
                width=200,
                height=60,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["warning"],
                command=self.export_attendance_to_excel
            )
            attendance_btn.pack(pady=10)

    def export_filtered_students_to_excel(self):
            """Export only filtered/search result students from the Treeview to Excel"""

            try:
                # Fetch all visible rows in Treeview
                items = self.student_tree.get_children()
                if not items:
                    return messagebox.showwarning("No Data", "No students to export!")

                # Extract data from Treeview items
                students = []
                for item in items:
                    values = self.student_tree.item(item)['values']
                    full_name = values[1]
                    first_name = full_name.split(' ')[0] if full_name else ''
                    last_name = ' '.join(full_name.split(' ')[1:]) if len(full_name.split(' ')) > 1 else ''
                    student = {
                        "student_id": values[0],
                        "first_name": first_name,
                        "last_name": last_name,
                        "gender": values[2],
                        "dob": values[3],
                        "email": values[4],
                        "phone": values[5],
                        "address": "",  # Address not in Treeview columns
                        "course_name": values[6],
                        "admission_date": values[7],
                        "status": values[8],
                    }
                    students.append(student)

                # Ask user where to save the Excel file
                filename_default = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    initialfile=filename_default,
                    title="Save Students As"
                )
                if not file_path:
                    return  # User cancelled dialog

                # Create workbook and fill data
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Students"

                headers = ["Student ID", "First Name", "Last Name", "Gender", "Date of Birth",
                           "Email", "Phone", "Address", "Course", "Admission Date", "Status"]

                for col, header in enumerate(headers, 1):
                    cell = ws.cell(row=1, column=col, value=header)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="1f538d", end_color="1f538d", fill_type="solid")
                    cell.alignment = Alignment(horizontal="center")

                for row, student in enumerate(students, 2):
                    ws.cell(row=row, column=1, value=student['student_id'])
                    ws.cell(row=row, column=2, value=student['first_name'])
                    ws.cell(row=row, column=3, value=student['last_name'])
                    ws.cell(row=row, column=4, value=student['gender'])
                    ws.cell(row=row, column=5, value=student['dob'])
                    ws.cell(row=row, column=6, value=student['email'])
                    ws.cell(row=row, column=7, value=student['phone'])
                    ws.cell(row=row, column=8, value=student['address'])
                    ws.cell(row=row, column=9, value=student['course_name'])
                    ws.cell(row=row, column=10, value=student['admission_date'])
                    ws.cell(row=row, column=11, value=student['status'])

                # Auto size columns
                for column in ws.columns:
                    max_length = 0
                    col_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if cell.value and len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    ws.column_dimensions[col_letter].width = max_length + 2

                wb.save(file_path)
                messagebox.showinfo("Success", f"Students exported successfully!\nFile: {file_path}")

            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

    def export_students_to_excel(self):
            """Export students data to Excel with progress"""

            try:
                students = self.db.get_all_students()

                if not students:
                    messagebox.showwarning("No Data", "No students to export!")
                    return

                # Create workbook
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Students"

                # Headers
                headers = ["Student ID", "First Name", "Last Name", "Gender", "Date of Birth",
                           "Email", "Phone", "Address", "Course", "Admission Date", "Status"]

                for col, header in enumerate(headers, 1):
                    cell = ws.cell(row=1, column=col, value=header)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="1f538d", end_color="1f538d", fill_type="solid")
                    cell.alignment = Alignment(horizontal="center")

                # Data rows
                for row, student in enumerate(students, 2):
                    ws.cell(row=row, column=1, value=student['student_id'])
                    ws.cell(row=row, column=2, value=student['first_name'])
                    ws.cell(row=row, column=3, value=student['last_name'])
                    ws.cell(row=row, column=4, value=student['gender'])
                    ws.cell(row=row, column=5, value=student['dob'].strftime('%Y-%m-%d') if student['dob'] else '')
                    ws.cell(row=row, column=6, value=student['email'])
                    ws.cell(row=row, column=7, value=student['phone'])
                    ws.cell(row=row, column=8, value=student['address'])
                    ws.cell(row=row, column=9, value=student.get('course_name', 'N/A'))
                    ws.cell(row=row, column=10,
                            value=student['admission_date'].strftime('%Y-%m-%d') if student['admission_date'] else '')
                    ws.cell(row=row, column=11, value=student['status'])

                # Auto-size columns
                for column in ws.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if cell.value and len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    ws.column_dimensions[column_letter].width = adjusted_width

                filename_default = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")],
                                                        initialfile=filename_default, title="Save Students Export As")
                if not filepath:
                    return  # User cancelled dialog

                wb.save(filepath)

                messagebox.showinfo("Success", f"Students exported successfully!\nFile: {filepath}")

            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

    def export_courses_to_excel(self):
            """Export courses to Excel"""

            try:
                courses = self.db.get_all_courses()

                if not courses:
                    messagebox.showwarning("No Data", "No courses to export!")
                    return

                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Courses"

                headers = ["Course ID", "Course Name", "Course Code", "Description",
                           "Duration (Months)", "Fees (₹)", "Students Enrolled"]

                for col, header in enumerate(headers, 1):
                    cell = ws.cell(row=1, column=col, value=header)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="14a085", end_color="14a085", fill_type="solid")
                    cell.alignment = Alignment(horizontal="center")

                for row, course in enumerate(courses, 2):
                    ws.cell(row=row, column=1, value=course['course_id'])
                    ws.cell(row=row, column=2, value=course['course_name'])
                    ws.cell(row=row, column=3, value=course['course_code'])
                    ws.cell(row=row, column=4, value=course['description'])
                    ws.cell(row=row, column=5, value=course['duration_months'])
                    ws.cell(row=row, column=6, value=float(course['fees']) if course['fees'] else 0)
                    ws.cell(row=row, column=7, value=course['student_count'])

                for column in ws.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if cell.value and len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    ws.column_dimensions[column_letter].width = max_length + 2

                filename_default = f"courses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")],
                                                        initialfile=filename_default, title="Save Courses Export As")
                if not filepath:
                    return  # User cancelled dialog

                wb.save(filepath)

                messagebox.showinfo("Success", f"Courses exported successfully!\nFile: {filepath}")

            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

    def export_attendance_to_excel(self):
            """Export attendance to Excel (with student and course names, filtered by date range)"""

            dialog = ctk.CTkToplevel(self)
            dialog.title("Export Attendance")
            dialog.geometry("400x270")
            dialog.transient(self)
            dialog.grab_set()

            ctk.CTkLabel(dialog, text="Export Attendance Records", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

            ctk.CTkLabel(dialog, text="Start Date:").pack(pady=5)
            start_date_entry = DateEntry(dialog, width=20, background=COLORS["primary"], foreground='white', borderwidth=2,
                                         date_pattern='yyyy-mm-dd')
            start_date_entry.pack(pady=5)

            ctk.CTkLabel(dialog, text="End Date:").pack(pady=5)
            end_date_entry = DateEntry(dialog, width=20, background=COLORS["primary"], foreground='white', borderwidth=2,
                                       date_pattern='yyyy-mm-dd')
            end_date_entry.pack(pady=5)

            def export():
                start_date = start_date_entry.get_date()
                end_date = end_date_entry.get_date()

                if start_date > end_date:
                    messagebox.showerror("Date Error", "Start date must be before end date")
                    return

                data = self.db.get_attendance_full_by_date_range(start_date, end_date)
                if not data:
                    messagebox.showwarning("No Data", "No attendance records found for the selected date range.")
                    return

                filename_default = f"attendance_export_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx"
                file_path = filedialog.asksaveasfilename(
                    defaultextension='.xlsx',
                    filetypes=[('Excel files', '*.xlsx')],
                    initialfile=filename_default,
                    title='Save Attendance Export As'
                )
                if not file_path:
                    return

                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Attendance"

                headers = ["Student ID", "Student Name", "Course Name", "Attendance Date", "Status", "Remarks"]

                for col, header in enumerate(headers, 1):
                    cell = ws.cell(row=1, column=col, value=header)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="f39c12", end_color="f39c12", fill_type="solid")
                    cell.alignment = Alignment(horizontal="center")

                for row, record in enumerate(data, 2):
                    ws.cell(row=row, column=1, value=record["student_id"])
                    ws.cell(row=row, column=2, value=record["student_name"])
                    ws.cell(row=row, column=3, value=record["course_name"])
                    ws.cell(row=row, column=4, value=record["attendance_date"].strftime("%Y-%m-%d"))
                    ws.cell(row=row, column=5, value=record["status"])
                    ws.cell(row=row, column=6, value=record["remarks"])

                for column in ws.columns:
                    max_length = 0
                    col_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if cell.value and len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    ws.column_dimensions[col_letter].width = max_length + 2

                wb.save(file_path)
                messagebox.showinfo("Success", f"Attendance exported successfully!\nFile: {file_path}")
                dialog.destroy()

            export_btn = ctk.CTkButton(dialog, text="Export", width=150, height=40, command=export)
            export_btn.pack(pady=20)
