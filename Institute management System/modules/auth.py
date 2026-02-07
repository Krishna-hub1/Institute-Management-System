import customtkinter as ctk
from tkinter import messagebox
import hashlib

from config import COLORS


class AuthModule:
    def __init__(self, app):
        self.app = app

        # inputs
        self.login_username = None
        self.login_password = None

        self.reg_fullname = None
        self.reg_username = None
        self.reg_email = None
        self.reg_password = None
        self.reg_confirm = None
        self.reg_role = None

        self.fp_email = None
        self.fp_new_password = None
        self.fp_confirm_password = None

    # ---------------- MAIN AUTH SCREEN ----------------

    def show_login_screen(self):
        self.app.clear_window()

        frame = ctk.CTkFrame(self.app, width=500, height=600, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            frame,
            text="Institute Management System",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=(30, 10))

        tabs = ctk.CTkTabview(frame, width=420, height=430)
        tabs.pack(padx=30, pady=20)

        tabs.add("Login")
        tabs.add("Register")

        self._build_login_tab(tabs.tab("Login"))
        self._build_register_tab(tabs.tab("Register"))

    # ---------------- LOGIN ----------------

    def _build_login_tab(self, parent):
        ctk.CTkLabel(parent, text="Username or Email").pack(pady=(30, 5))
        self.login_username = ctk.CTkEntry(parent, width=320, height=40)
        self.login_username.pack(pady=5)

        ctk.CTkLabel(parent, text="Password").pack(pady=(15, 5))
        self.login_password = ctk.CTkEntry(parent, width=320, height=40, show="*")
        self.login_password.pack(pady=5)

        ctk.CTkButton(
            parent,
            text="Login",
            width=320,
            height=45,
            fg_color=COLORS["success"],
            command=self.login
        ).pack(pady=20)

        forgot_lbl = ctk.CTkLabel(
            parent,
            text="Forgot Password?",
            text_color=COLORS["info"],
            cursor="hand2"
        )
        forgot_lbl.pack(pady=(5, 0))
        forgot_lbl.bind("<Button-1>", lambda e: self.show_forgot_password())


    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Error", "Enter username and password")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = self.app.db.authenticate_user(username, password_hash)

        if not user:
            messagebox.showerror("Login Failed", "Invalid credentials")
            return

        self.app.current_user = user
        messagebox.showinfo("Success", f"Welcome {user['full_name']}")

        self.app.build_main_layout()

    # ---------------- REGISTER ----------------

    def _build_register_tab(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, width=380, height=360)
        scroll.pack(pady=10)

        self.reg_fullname = self._entry(scroll, "Full Name")
        self.reg_username = self._entry(scroll, "Username")
        self.reg_email = self._entry(scroll, "Email")
        self.reg_password = self._entry(scroll, "Password", True)
        self.reg_confirm = self._entry(scroll, "Confirm Password", True)

        ctk.CTkLabel(scroll, text="Role").pack(pady=(10, 5))
        self.reg_role = ctk.CTkOptionMenu(scroll, values=["Admin", "Staff"])
        self.reg_role.pack(pady=5)

        ctk.CTkButton(
            scroll,
            text="Register",
            width=300,
            height=40,
            fg_color=COLORS["info"],
            command=self.register
        ).pack(pady=20)

    def register(self):
        full = self.reg_fullname.get().strip()
        user = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        pwd = self.reg_password.get().strip()
        confirm = self.reg_confirm.get().strip()
        role = self.reg_role.get()

        if not all([full, user, email, pwd, confirm]):
            messagebox.showwarning("Error", "All fields required")
            return

        if pwd != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(pwd) < 6:
            messagebox.showwarning("Error", "Password must be at least 6 characters")
            return

        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        success, msg = self.app.db.add_user((user, email, pwd_hash, full, role))

        if success:
            messagebox.showinfo("Success", msg)
            self.show_login_screen()
        else:
            messagebox.showerror("Error", msg)

    # ---------------- FORGOT PASSWORD ----------------

    def show_forgot_password(self):
        self.app.clear_window()

        frame = ctk.CTkFrame(self.app, width=450, height=420, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            frame,
            text="Reset Password",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=30)

        self.fp_email = ctk.CTkEntry(frame, width=320, height=40, placeholder_text="Registered Email")
        self.fp_email.pack(pady=10)

        self.fp_new_password = ctk.CTkEntry(frame, width=320, height=40, show="*", placeholder_text="New Password")
        self.fp_new_password.pack(pady=10)

        self.fp_confirm_password = ctk.CTkEntry(frame, width=320, height=40, show="*", placeholder_text="Confirm Password")
        self.fp_confirm_password.pack(pady=10)

        ctk.CTkButton(
            frame,
            text="Reset Password",
            width=320,
            height=45,
            fg_color=COLORS["success"],
            command=self.reset_password
        ).pack(pady=20)

        ctk.CTkButton(
            frame,
            text="Back to Login",
            fg_color=COLORS["danger"],
            command=self.show_login_screen
        ).pack()

    def reset_password(self):
        email = self.fp_email.get().strip()
        pwd = self.fp_new_password.get().strip()
        confirm = self.fp_confirm_password.get().strip()

        if not email or not pwd or not confirm:
            messagebox.showwarning("Error", "All fields required")
            return

        if pwd != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        user = self.app.db.get_user_by_email(email)
        if not user:
            messagebox.showerror("Error", "Email not registered")
            return

        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        success, msg = self.app.db.update_password(email, pwd_hash)

        if success:
            messagebox.showinfo("Success", "Password updated")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", msg)

    # ---------------- UTIL ----------------

    def _entry(self, parent, label, password=False):
        ctk.CTkLabel(parent, text=label).pack(pady=(10, 5))
        e = ctk.CTkEntry(parent, width=300, height=35, show="*" if password else "")
        e.pack(pady=5)
        return e
