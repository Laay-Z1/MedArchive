import tkinter as tk
from tkinter import ttk, messagebox

from services.auth_service import authenticate_user, register_user
from ui.main_window import MainWindow


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("МедАрхив — вход")
        self.root.geometry("440x510")
        self.root.minsize(400, 450)
        self.root.configure(bg="#F6FAF9")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#F6FAF9")
        self.style.configure("TLabel", background="#F6FAF9", foreground="#172B35",
                             font=("Arial", 11))
        self.style.configure("Title.TLabel", font=("Arial", 25, "bold"),
                             foreground="#087F75")
        self.style.configure("TButton", font=("Arial", 11, "bold"), padding=9)
        self.style.configure("TEntry", padding=8)

        self.frame = ttk.Frame(root, padding=32)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        ttk.Label(self.frame, text="♥  МедАрхив", style="Title.TLabel").pack(pady=(20, 8))
        ttk.Label(self.frame, text="Войдите в свою медицинскую карту").pack(pady=(0, 22))

        ttk.Label(self.frame, text="Логин").pack(anchor="w")
        self.login_entry = ttk.Entry(self.frame)
        self.login_entry.pack(fill="x", pady=(5, 12))

        ttk.Label(self.frame, text="Пароль").pack(anchor="w")
        self.password_entry = ttk.Entry(self.frame, show="•")
        self.password_entry.pack(fill="x", pady=(5, 18))

        ttk.Button(self.frame, text="Войти", command=self._login).pack(fill="x")
        ttk.Separator(self.frame).pack(fill="x", pady=20)

        ttk.Label(self.frame, text="Нет аккаунта? Создайте его").pack(pady=(0, 8))
        ttk.Button(self.frame, text="Регистрация", command=self._open_registration).pack(fill="x")

    def _login(self):
        try:
            user = authenticate_user(self.login_entry.get(), self.password_entry.get())
            if user is None:
                messagebox.showwarning("Вход", "Неверный логин или пароль.")
                return
            self.root.destroy()
            app_root = tk.Tk()
            MainWindow(app_root, user)
            app_root.mainloop()
        except Exception as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _open_registration(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Регистрация")
        dialog.geometry("370x330")
        dialog.configure(bg="#F6FAF9")
        frame = ttk.Frame(dialog, padding=24)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Создание аккаунта", style="Title.TLabel").pack(pady=(0, 16))
        fields = {}
        for key, label in (("name", "ФИО"), ("login", "Логин"), ("password", "Пароль (от 8 символов)")):
            ttk.Label(frame, text=label).pack(anchor="w")
            entry = ttk.Entry(frame, show="•" if key == "password" else "")
            entry.pack(fill="x", pady=(4, 10))
            fields[key] = entry

        def create_account():
            try:
                register_user(fields["login"].get(), fields["password"].get(), fields["name"].get())
                messagebox.showinfo("Регистрация", "Аккаунт создан. Теперь войдите.")
                self.login_entry.delete(0, "end")
                self.login_entry.insert(0, fields["login"].get())
                dialog.destroy()
            except Exception as exc:
                messagebox.showwarning("Регистрация", str(exc))

        ttk.Button(frame, text="Создать аккаунт", command=create_account).pack(fill="x", pady=8)
