import tkinter as tk
from tkinter import messagebox

from database.db import initialize_database
from ui.login_window import LoginWindow


def main():
    try:
        initialize_database()
    except Exception as exc:
        messagebox.showerror("Ошибка базы данных", str(exc))
        return

    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
