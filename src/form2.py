from tkinter import Tk,Entry,Button, NW,Frame, Label, Canvas, Scrollbar, messagebox,Toplevel
from db import *
from db import Session, ProductTypeImport, Employee
def open_modal_window():
    form={}
    # languages = ["Python", "C#", "Java", "JavaScript"]
    # combobox = ttk.Combobox(values=languages)
    # combobox.pack(anchor=NW, padx=6, pady=6)
    def add_record():
        data={}
        for column in columns:
            field={}
            if column.name !='id':
                data[ column.name] = form[column.name]['entry'].get()
        messagebox.showinfo(
            str(data)
        )
    modal = Toplevel()
    modal.title("Модальное окно")
    modal.geometry("800x600")
    modal.grab_set()
    columns = Employee.__table__.columns

    for column in columns:
        field={}
        if column.name !='id':
            desk= column.comment  if column.comment else  column.comment
            field['label']= Label(modal, text=desk)
            field['label'].pack(anchor=NW, padx=8 )
            field['entry']= Entry(modal,width=120)
            field['entry'].pack(anchor=NW, padx=8)
            form[column.name]=field

    btn_close = Button(modal, text="Добавить запись", command=add_record)
    btn_close.pack(anchor=NW, padx=8, pady=8)

    btn_close = Button(modal, text="Выход", command=modal.destroy)
    btn_close.pack(anchor=NW, padx=8, pady=8)



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
