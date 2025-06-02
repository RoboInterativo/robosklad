from tkinter import Tk,Entry,Button, NW,Frame, Label, Canvas, Scrollbar, messagebox,Toplevel
from db import *
from db import Session, ProductTypeImport, Employee

from tkinter import Toplevel, Label, Entry, Button, NW, messagebox
from tkinter import ttk


def open_modal_window():
    form = {}
    session = Session()  # Создаем сессию для работы с БД

    def add_record():
        data = {}
        for column in columns:
            if column.name != 'id':
                # Для Combobox берем значение, а не текст
                if isinstance(form[column.name]['widget'], ttk.Combobox):
                    data[column.name] = form[column.name]['widget'].get()
                else:
                    data[column.name] = form[column.name]['widget'].get()

        messagebox.showinfo("Данные", str(data))
        # Здесь можно добавить сохранение в БД

    modal = Toplevel()
    modal.title("Модальное окно")
    modal.geometry("800x600")
    modal.grab_set()

    columns = ProductsImport.__table__.columns

    for column in columns:
        if column.name != 'id':
            # Создаем метку
            label_text = column.comment if column.comment else column.name
            Label(modal, text=label_text).pack(anchor=NW, padx=8)

            # Проверяем, является ли поле ForeignKey
            if column.foreign_keys:
                # Получаем связанную модель
                fk = list(column.foreign_keys)[0]
                related_model = fk.column.table

                # Получаем все записи из связанной таблицы
                related_objects = session.query(related_model).all()

                # Создаем Combobox с значениями
                cb = ttk.Combobox(modal, width=117)

                # Формируем список отображаемых значений
                display_values = [str(obj) for obj in related_objects]
                cb['values'] = display_values

                # Сохраняем оригинальные объекты для сопоставления
                cb.related_objects = {str(obj): obj.id for obj in related_objects}

                cb.pack(anchor=NW, padx=8)
                form[column.name] = {'widget': cb}
            else:
                # Обычное текстовое поле для не-FK полей
                entry = Entry(modal, width=120)
                entry.pack(anchor=NW, padx=8)
                form[column.name] = {'widget': entry}

    Button(modal, text="Добавить запись", command=add_record).pack(anchor=NW, padx=8, pady=8)
    Button(modal, text="Выход", command=modal.destroy).pack(anchor=NW, padx=8, pady=8)
# def open_modal_window():
#     form={}
#     # languages = ["Python", "C#", "Java", "JavaScript"]
#     # combobox = ttk.Combobox(values=languages)
#     # combobox.pack(anchor=NW, padx=6, pady=6)
#     def add_record():
#         data={}
#         for column in columns:
#             field={}
#             if column.name !='id':
#                 data[ column.name] = form[column.name]['entry'].get()
#         messagebox.showinfo(
#             str(data)
#         )
#     modal = Toplevel()
#     modal.title("Модальное окно")
#     modal.geometry("800x600")
#     modal.grab_set()
#     columns = Employee.__table__.columns
#
#     for column in columns:
#         field={}
#         if column.name !='id':
#             desk= column.comment  if column.name else  column.comment
#             field['label']= Label(modal, text=desk)
#             field['label'].pack(anchor=NW, padx=8 )
#             field['entry']= Entry(modal,width=120)
#             field['entry'].pack(anchor=NW, padx=8)
#             form[column.name]=field
#
#     btn_close = Button(modal, text="Добавить запись", command=add_record)
#     btn_close.pack(anchor=NW, padx=8, pady=8)
#
#     btn_close = Button(modal, text="Выход", command=modal.destroy)
#     btn_close.pack(anchor=NW, padx=8, pady=8)



def show_partners(root, partners):
    """Упрощенный вариант отображения карточек партнеров с прокруткой"""
    # Основной контейнер
    container = Frame(root)
    container.pack(fill="both", expand=True)

    # Настройка прокрутки
    canvas = Canvas(container)
    scrollbar = Scrollbar(container, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Фрейм для карточек внутри canvas
    cards_frame = Frame(canvas)
    canvas.create_window((0, 0), window=cards_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    cards_frame.bind("<Configure>", on_frame_configure)
    # Функция обработки клика по карточке
    def on_card_click(partner_data):
        # Здесь можно выполнить любые действия с данными партнера
        messagebox.showinfo(
            "Выбран партнер",
            f"{partner_data['name']}\n"
            f"Телефон: {partner_data['phone']}\n"
            f"Рейтинг: {partner_data['rating']}%"
        )
        # Или например открыть подробную информацию:
        # show_partner_details(partner_data)
    # Создаем карточки партнеров
    for partner in partners:
        card = Frame(cards_frame, bd=1, relief="solid", padx=10, pady=5)
        card.pack(fill="x", pady=2)
           # Делаем всю карточку кликабельной
        card.bind("<Button-1>", lambda e, p=partner: on_card_click(p))

        # Первая строка: Название и рейтинг
        Label(card, text=f"{partner['type']} | {partner['name']}").pack(anchor="w")
        Label(card, text=f"Рейтинг: {partner['rating']}%", fg="blue").pack(anchor="e", side="right")

        # Вторая строка: Должность
        Label(card, text=partner['position']).pack(anchor="w")

        # Третья строка: Телефон
        Label(card, text=partner['phone']).pack(anchor="w")
