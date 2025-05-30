from tkinter import *
from db import *

from db import Session, Employee
from datetime import datetime

def add_employee():
    # Создаем сессию
    session = Session()

    try:
        # Создаем нового сотрудника
        new_employee = Employee(
            full_name="Иванов Иван Иванович",
            birth_date=datetime(1985, 5, 15),
            passport_data="4510 123456",
            bank_details="Сбербанк 40817810000000000000",
            has_family=True,
            health_status="Здоров",
            contact_phone="+79161234567",
            email="ivanov@example.com"
        )

        # Добавляем и сохраняем
        session.add(new_employee)
        session.commit()
        print(f"Добавлен сотрудник с ID: {new_employee.id}")

    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()



def open_modal_window():
    modal = Toplevel()
    modal.title("Модальное окно")
    modal.geometry("800x600")
    modal.grab_set()  # Блокирует главное окно

    label = Label(modal, text="ФИО")
    label.pack(anchor=NW, padx=8, pady= 8)
    entry=Entry(modal)
    entry.pack(anchor=NW, padx=8, pady= 8)
    btn_close = Button(modal, text="OK", command=modal.destroy)
    btn_close.pack(anchor=NW, padx=8, pady= 8)



def main():
    # print(test)
    root = Tk()     # создаем корневой объект - окно
    root.title("Приложение на Tkinter")     # устанавливаем заголовок окна
    root.geometry("800x600")    # устанавливаем размеры окна
    # Пытаемся загрузить иконку (если есть)
    try:
        root.iconbitmap("src/static/app.ico")  # путь к иконке
    except:
        print("Иконка не загружена!")  # можно пропустить или заменить на стандартную
    # root.iconbitmap("src/static/icon.ico")  # Укажите путь к файлу .ico
    label = Label(text="Hello METANIT.COM") # создаем текстовую метку
    label.pack()    # размещаем метку в окне
    btn_modal = Button(root, text="Открыть модальное окно", command=open_modal_window)
    btn_modal.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
