import tkinter as tk
from tkinter import ttk


class MainWindow:
    PAGES = [
        "Главная", "Медицинская карта", "Лекарства",
        "План лечения", "Документы", "Настройки"
    ]

    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("МедАрхив")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#F6FAF9")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#F6FAF9")
        self.style.configure("Sidebar.TFrame", background="#EAF5F2")
        self.style.configure("TLabel", background="#F6FAF9", foreground="#172B35",
                             font=("Arial", 11))
        self.style.configure("Heading.TLabel", font=("Arial", 23, "bold"),
                             foreground="#153A3A")
        self.style.configure("Brand.TLabel", background="#EAF5F2",
                             foreground="#078F83", font=("Arial", 20, "bold"))
        self.style.configure("Nav.TButton", anchor="w", padding=12,
                             background="#EAF5F2", foreground="#23413F")
        self.style.map("Nav.TButton", background=[("active", "#D9EFEB")])

        container = ttk.Frame(root)
        container.pack(fill="both", expand=True)

        sidebar = ttk.Frame(container, style="Sidebar.TFrame", padding=18)
        sidebar.pack(side="left", fill="y")
        sidebar.configure(width=245)
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="♥  МедАрхив", style="Brand.TLabel").pack(anchor="w", pady=(8, 28))
        self.content = ttk.Frame(container, padding=34)
        self.content.pack(side="left", fill="both", expand=True)

        for page_name in self.PAGES:
            ttk.Button(
                sidebar, text=page_name, style="Nav.TButton",
                command=lambda name=page_name: self.show_page(name)
            ).pack(fill="x", pady=3)

        ttk.Label(sidebar, text=f"Пользователь:\n{user['full_name']}",
                  background="#EAF5F2").pack(side="bottom", anchor="w", pady=12)

        self.show_page("Главная")

    def show_page(self, name):
        for child in self.content.winfo_children():
            child.destroy()

        ttk.Label(self.content, text=name, style="Heading.TLabel").pack(anchor="w", pady=(0, 12))
        ttk.Label(
            self.content,
            text=f"Раздел «{name}». Здесь будет реализован функционал.",
            wraplength=800
        ).pack(anchor="w")

        if name == "Главная":
            ttk.Label(
                self.content,
                text=f"Добро пожаловать, {self.user['full_name']}!",
                font=("Arial", 15, "bold")
            ).pack(anchor="w", pady=24)
            ttk.Label(
                self.content,
                text="Выберите раздел слева, чтобы работать со своей медицинской историей."
            ).pack(anchor="w")
