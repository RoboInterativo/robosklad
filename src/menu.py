
from tkinter import Menu, messagebox
from form2 import *
def create_main_menu(root):
    """Создает главное меню для приложения"""
    menubar = Menu(root)


    # Меню партнеры
    partner_menu = Menu(menubar, tearoff=0)
    partner_menu.add_command(label="Добавить", command=lambda: messagebox.showinfo("New", "New file"))

    # Настройки
    settings_menu = Menu(menubar, tearoff=0)
    settings_menu.add_command(label="Импорт данных", command=open_modal_window)

    menubar.add_cascade(label="Партнеры", menu=partner_menu)
    menubar.add_cascade(label="Настройки", menu=settings_menu)




    # Устанавливаем меню в окно
    root.config(menu=menubar)

    return menubar
