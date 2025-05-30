
from tkinter import Menu, messagebox

def create_main_menu(root):
    """Создает главное меню для приложения"""
    menubar = Menu(root)


    # Меню партнеры
    partner_menu = Menu(menubar, tearoff=0)
    partner_menu.add_command(label="Добавить", command=lambda: messagebox.showinfo("New", "New file"))


    menubar.add_cascade(label="Партнеры", menu=partner_menu)


    # Устанавливаем меню в окно
    root.config(menu=menubar)

    return menubar
