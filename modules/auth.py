import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import hashlib
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import SMTP_CONFIG, COLORS



class AuthModule:
    """Feature module extracted from the original application."""

    def show_login_screen(self):
            """Display login/register screen"""
            # Clear window
            self.configure(fg_color="#F1F5F9")
            for widget in self.winfo_children():
                widget.destroy()

            # Login Frame - Centered
            login_frame = ctk.CTkFrame(self, width=520, height=620, corner_radius=24, fg_color="#FFFFFF")
                            
            login_frame.place(relx=0.5, rely=0.5, anchor="center")

            # Title
            title = ctk.CTkLabel(
                login_frame,
                text="Institute Management System",
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color="#1E3A8A"
            )
            title.pack(pady=(40, 10))

            subtitle = ctk.CTkLabel(
                login_frame,
                text="Secure Login Portal",
                font=ctk.CTkFont(size=14),
                text_color="#64748B"
            )
            subtitle.pack(pady=(0, 30))

            # Login/Register Tabs
            self.auth_tabview = ctk.CTkTabview(
                login_frame,
                width=420,
                height=400,
                corner_radius=12,
                fg_color="#F8FAFC",
                segmented_button_fg_color="#E8EEF7",
                segmented_button_selected_color="#2563EB",
                segmented_button_selected_hover_color="#1D4ED8",
                segmented_button_unselected_color="#E8EEF7",
                segmented_button_unselected_hover_color="#D7E1EF"
            )
            self.auth_tabview.pack(pady=20, padx=30)

            self.auth_tabview.add("Login")
            self.auth_tabview.add("Register")

            # Professional Login / Register tab colors
            self.auth_tabview.configure(
                text_color="#1E293B"
            )
            self.auth_tabview._segmented_button.configure(
                text_color="#475569",
                selected_hover_color="#1D4ED8",
                selected_color="#2563EB",
                unselected_color="#E8EEF7",
                unselected_hover_color="#D7E1EF"
            )

            # === LOGIN TAB ===
            login_tab = self.auth_tabview.tab("Login")

            # === USERNAME ===
            ctk.CTkLabel(
                login_tab,
                text="Username or Email",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#1E293B"
            ).pack(pady=(20, 5), padx=35, anchor="w")

            username_frame = ctk.CTkFrame(
                login_tab,
                width=350,
                height=45,
                corner_radius=8,
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#CBD5E1"
            )
            username_frame.pack(pady=5)
            username_frame.pack_propagate(False)

            # User icon
            user_icon = tk.Canvas(
                username_frame,
                width=28,
                height=28,
                bg="#FFFFFF",
                highlightthickness=0
            )
            user_icon.pack(side="left", padx=(8, 2))
            user_icon.create_oval(10, 4, 18, 12, outline="#94A3B8", width=1.5)
            user_icon.create_arc(6, 11, 22, 26, start=0, extent=180, outline="#94A3B8", width=1.5)

            self.login_username = ctk.CTkEntry(
                username_frame,
                height=40,
                border_width=0,
                corner_radius=0,
                fg_color="transparent",
                text_color="#1E293B",
                placeholder_text="Enter username or email",
                placeholder_text_color="#94A3B8"
            )
            self.login_username.pack(side="left", fill="x", expand=True, padx=(0, 8))


            # === PASSWORD ===
            ctk.CTkLabel(
                login_tab,
                text="Password",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#1E293B"
            ).pack(pady=(15, 5), padx=35, anchor="w")

            password_frame = ctk.CTkFrame(
                login_tab,
                width=350,
                height=45,
                corner_radius=8,
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#CBD5E1"
            )
            password_frame.pack(pady=5)
            password_frame.pack_propagate(False)

            # Lock icon
            lock_icon = tk.Canvas(
                password_frame,
                width=28,
                height=28,
                bg="#FFFFFF",
                highlightthickness=0
            )
            lock_icon.pack(side="left", padx=(8, 2))
            lock_icon.create_arc(9, 3, 19, 15, start=0, extent=180, outline="#94A3B8", width=1.5)
            lock_icon.create_rectangle(7, 11, 21, 23, outline="#94A3B8", width=1.5)
            lock_icon.create_oval(13, 15, 15, 18, fill="#94A3B8", outline="#94A3B8")

            self.login_password = ctk.CTkEntry(
                password_frame,
                height=40,
                border_width=0,
                corner_radius=0,
                fg_color="transparent",
                text_color="#1E293B",
                placeholder_text="Enter password",
                placeholder_text_color="#94A3B8",
                show="*"
            )
            self.login_password.pack(side="left", fill="x", expand=True, padx=(0, 2))

            # Show / Hide password
            self.password_visible = False

            self.eye_button = ctk.CTkButton(
                password_frame,
                text="◉",
                width=32,
                height=32,
                corner_radius=5,
                fg_color="transparent",
                hover_color="#EFF6FF",
                text_color="#94A3B8",
                font=ctk.CTkFont(size=15),
                command=self.toggle_password
            )
            self.eye_button.pack(side="right", padx=5)

            self.login_password.bind('<Return>', lambda e: self.login())

            # self.login_username.insert(0, 'faiz')
            # self.login_password.insert(0, '123456')

            login_btn = ctk.CTkButton(
                login_tab,
                text="Login",
                width=350,
                height=45,
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=COLORS["primary"],
                hover_color=COLORS["secondary"],
                command=self.login
            )
            login_btn.pack(pady=20)

            forgot_btn = ctk.CTkButton(
                login_tab,
                text="Forgot Password?",
                width=200,
                height=30,
                corner_radius=0,
                fg_color="transparent",
                hover_color="#EFF6FF",
                text_color="#2563EB",
                font=ctk.CTkFont(size=13),
                command=self.show_forgot_password
            )
            forgot_btn.pack(pady=5)

            # === REGISTER TAB ===
            register_tab = self.auth_tabview.tab("Register")

            # Make register tab scrollable
            register_scroll = ctk.CTkScrollableFrame(register_tab, width=380, height=280)
            register_scroll.pack(fill="both", expand=True, pady=10)

            ctk.CTkLabel(register_scroll, text="Full Name", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
            self.reg_fullname = ctk.CTkEntry(register_scroll, width=350, height=35)
            self.reg_fullname.pack(pady=5)

            ctk.CTkLabel(register_scroll, text="Username", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
            self.reg_username = ctk.CTkEntry(register_scroll, width=350, height=35)
            self.reg_username.pack(pady=5)

            ctk.CTkLabel(register_scroll, text="Email", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
            self.reg_email = ctk.CTkEntry(register_scroll, width=350, height=35)
            self.reg_email.pack(pady=5)

            ctk.CTkLabel(register_scroll, text="Password", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
            self.reg_password = ctk.CTkEntry(register_scroll, width=350, height=35, show="*")
            self.reg_password.pack(pady=5)

            ctk.CTkLabel(register_scroll, text="Confirm Password", font=ctk.CTkFont(size=12, weight="bold")).pack(
                pady=(10, 5))
            self.reg_confirm_password = ctk.CTkEntry(register_scroll, width=350, height=35, show="*")
            self.reg_confirm_password.pack(pady=5)

            ctk.CTkLabel(register_scroll, text="Role", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
            self.reg_role = ctk.CTkOptionMenu(register_scroll, width=350, height=35, values=["Admin", "Staff"])
            self.reg_role.pack(pady=5)

            register_btn = ctk.CTkButton(
                register_scroll,
                text="Register Account",
                width=350,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#1D4ED8",
                hover_color="#1E40AF",
                command=self.register
            )
            register_btn.pack(pady=20)

    def toggle_password(self):
        """Show or hide the password."""
        if self.password_visible:
            self.login_password.configure(show="*")
            self.password_visible = False
        else:
            self.login_password.configure(show="")
            self.password_visible = True


    def login(self):
            """Handle user login"""
            username = self.login_username.get().strip()
            password = self.login_password.get().strip()

            if not username or not password:
                messagebox.showwarning("Input Error", "Please enter both username and password!")
                return

            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            # Authenticate
            user = self.db.authenticate_user(username, password_hash)

            if user:
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome {user['full_name']}!")
                self.show_main_application()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password!")

    def register(self):
            """Handle user registration"""
            fullname = self.reg_fullname.get().strip()
            username = self.reg_username.get().strip()
            email = self.reg_email.get().strip()
            password = self.reg_password.get().strip()
            confirm_password = self.reg_confirm_password.get().strip()
            role = self.reg_role.get()

            # Validation
            if not all([fullname, username, email, password, confirm_password]):
                messagebox.showwarning("Input Error", "Please fill all fields!")
                return

            if password != confirm_password:
                messagebox.showerror("Password Error", "Passwords do not match!")
                return

            if len(password) < 6:
                messagebox.showwarning("Password Error", "Password must be at least 6 characters!")
                return

            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            # Add user
            user_data = (username, email, password_hash, fullname, role)
            success, message = self.db.add_user(user_data)

            if success:
                messagebox.showinfo("Success", message)
                self.auth_tabview.set("Login")
                # Clear registration fields
                self.reg_fullname.delete(0, 'end')
                self.reg_username.delete(0, 'end')
                self.reg_email.delete(0, 'end')
                self.reg_password.delete(0, 'end')
                self.reg_confirm_password.delete(0, 'end')
            else:
                messagebox.showerror("Registration Failed", message)

    def show_forgot_password(self):
            """Show forgot password dialog"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Forgot Password")
            dialog.geometry("400x300")
            dialog.transient(self)
            dialog.grab_set()

            ctk.CTkLabel(dialog, text="Reset Password", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

            ctk.CTkLabel(dialog, text="Enter your email address:").pack(pady=10)
            email_entry = ctk.CTkEntry(dialog, width=300)
            email_entry.pack(pady=5)

            def send_reset_code():
                email = email_entry.get().strip()
                if not email:
                    messagebox.showwarning("Input Error", "Please enter email!")
                    return

                user = self.db.get_user_by_email(email)
                if not user:
                    messagebox.showerror("Error", "Email not found!")
                    return

                # Generate reset code
                reset_code = ''.join(random.choices(string.digits, k=6))

                # Send email (if SMTP configured)
                try:
                    msg = MIMEMultipart()
                    msg['From'] = SMTP_CONFIG['user']
                    msg['To'] = email
                    msg['Subject'] = "Password Reset Code"

                    body = f"""
                    Hello {user['full_name']},

                    Your password reset code is: {reset_code}

                    This code will expire in 10 minutes.

                    If you didn't request this, please ignore this email.

                    Best regards,
                    Student Management System
                    """

                    msg.attach(MIMEText(body, 'plain'))

                    server = smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port'])
                    server.starttls()
                    server.login(SMTP_CONFIG['user'], SMTP_CONFIG['password'])
                    server.send_message(msg)
                    server.quit()

                    # Show dialog to enter code and new password
                    dialog.destroy()
                    self.show_reset_password_dialog(email, reset_code)

                except Exception as e:
                    messagebox.showwarning("Email Error", f"Could not send email. Using temporary code: {reset_code}")
                    dialog.destroy()
                    self.show_reset_password_dialog(email, reset_code)

            send_btn = ctk.CTkButton(dialog, text="Send Reset Code", width=200, command=send_reset_code)
            send_btn.pack(pady=20)

    def show_reset_password_dialog(self, email, correct_code):
            """Show dialog to reset password with code"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Reset Password")
            dialog.geometry("400x350")
            dialog.transient(self)
            dialog.grab_set()

            ctk.CTkLabel(dialog, text="Enter Reset Code", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

            ctk.CTkLabel(dialog, text="Reset Code:").pack(pady=5)
            code_entry = ctk.CTkEntry(dialog, width=300)
            code_entry.pack(pady=5)

            ctk.CTkLabel(dialog, text="New Password:").pack(pady=5)
            new_pass = ctk.CTkEntry(dialog, width=300, show="*")
            new_pass.pack(pady=5)

            ctk.CTkLabel(dialog, text="Confirm Password:").pack(pady=5)
            confirm_pass = ctk.CTkEntry(dialog, width=300, show="*")
            confirm_pass.pack(pady=5)

            def reset_password():
                code = code_entry.get().strip()
                password = new_pass.get().strip()
                confirm = confirm_pass.get().strip()

                if code != correct_code:
                    messagebox.showerror("Error", "Invalid reset code!")
                    return

                if not password or len(password) < 6:
                    messagebox.showwarning("Error", "Password must be at least 6 characters!")
                    return

                if password != confirm:
                    messagebox.showerror("Error", "Passwords do not match!")
                    return

                # Update password
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                success, message = self.db.update_password(email, password_hash)

                if success:
                    messagebox.showinfo("Success", "Password reset successfully!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message)

            reset_btn = ctk.CTkButton(dialog, text="Reset Password", width=200, command=reset_password)
            reset_btn.pack(pady=20)
