from tkinter import *
from tkinter import messagebox, ttk
from db import Session, PartnersImport
from datetime import datetime
import re
from menu import create_main_menu
from form2 import *

def get_partners_data(session):
    try:
        # Запрос всех партнеров из таблицы PartnersImport
        partners = session.query(PartnersImport).all()
        # Преобразуем данные в список словарей
        partners_data = [
            {
                "id": partner.id,
                "type": partner.partner_type or "",
                "name": partner.company_name,
                "position": partner.director_name or "",
                "phone": partner.phone or "",
                "rating": partner.rating or 0
            }
            for partner in partners
        ]
        return partners_data
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные партнеров: {e}")
        return []

def main():
    root = Tk()
    root.title("Система управления партнёрами")
    root.geometry("800x600")

    # Создаем сессию для работы с базой данных
    session = Session()

    # Создаем и инициализируем меню
    create_main_menu(root)

    # Получаем данные партнеров из базы
    partners_data = get_partners_data(session)

    # Отображаем список партнеров
    show_partners(root, partners_data)

    # Закрываем сессию при закрытии приложения
    def on_closing():
        session.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
