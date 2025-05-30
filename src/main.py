from tkinter import *
from tkinter import messagebox, ttk
from db import *
from db import Session, ProductTypeImport, Employee
from datetime import datetime
import re
from  menu import *
from form2 import *




def main():
    root = Tk()
    root.title("Система управления партнёрами")
    root.geometry("800x600")

    # Создаем и инициализируем меню
    create_main_menu(root)
    # Пример данных партнеров
    partners_data = [
        {
            "type": "Тип 1",
            "name": "Наименование партнера",
            "position": "Директор",
            "phone": "+7 223 322 22 32",
            "rating": 10
        },
        {
            "type": "Тип 2",
            "name": "Другой партнер",
            "position": "Менеджер",
            "phone": "+7 111 222 33 44",
            "rating": 8
        },
        # Добавьте больше партнеров по аналогии
    ]

    show_partners(root, partners_data)
    root.mainloop()

if __name__ == '__main__':
    main()
