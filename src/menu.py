from tkinter import Menu, messagebox
from form2 import *
from db import *

def create_main_menu(root):
    """Создает главное меню для приложения"""
    menubar = Menu(root)

    # Меню партнеры
    partner_menu = Menu(menubar, tearoff=0)
    partner_menu.add_command(label="Добавить", command=lambda: open_modal_window(PartnersImport))

    # # Настройки
    settings_menu = Menu(menubar, tearoff=0)
    settings_menu.add_command(label="ProductTypeImport", command=lambda: open_modal_window2(ProductTypeImport))
    settings_menu.add_command(label="ProductTypeImport list", command=lambda: open_table_view_window(ProductTypeImport))

    settings_menu.add_command(label="ProductsImport", command=lambda: open_modal_window2(ProductsImport))
    settings_menu.add_command(label="ProductsImport list", command=lambda: open_table_view_window(ProductsImport))

    settings_menu.add_command(label="PartnerProductsImport", command=lambda: open_modal_window2(PartnerProductsImport))
    settings_menu.add_command(label="PartnerProductsImport list", command=lambda: open_table_view_window(PartnerProductsImport))


    menubar.add_cascade(label="Партнеры", menu=partner_menu)
    menubar.add_cascade(label="Настройки", menu=settings_menu)

    # Устанавливаем меню в окно
    root.config(menu=menubar)

    return menubar
