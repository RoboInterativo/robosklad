from tkinter import *
#Tk,Entry,BOTH,Button, NW,Frame, Label, Canvas, Scrollbar, messagebox,Toplevel
from db import *
# from db import Session, ProductTypeImport, Employee

from tkinter import Toplevel, Label, Entry, Button, NW, messagebox
from tkinter import ttk

from db import *
#import Session, PartnersImport
from sqlalchemy.exc import SQLAlchemyError


def open_table_view_window(table):
    """Открывает модальное окно со списком всех записей из указанной таблицы"""
    session = Session()  # Создаем сессию для работы с БД

    modal = Toplevel()
    modal.title(f"Список записей: {table.__tablename__}")
    modal.geometry("800x600")
    modal.grab_set()

    # Создаем фрейм для таблицы
    frame = Frame(modal)
    frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Получаем столбцы таблицы
    columns = table.__table__.columns
    column_names = [column.name for column in columns]
    column_headers = [column.comment if column.comment else column.name for column in columns]

    # Создаем Treeview для отображения данных
    tree = ttk.Treeview(frame, columns=column_names, show="headings")

    # Устанавливаем заголовки столбцов
    for name, header in zip(column_names, column_headers):
        tree.heading(name, text=header)
        tree.column(name, width=120, anchor=CENTER)

    # Добавляем полосу прокрутки
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)

    try:
        # Загружаем все записи из таблицы
        records = session.query(table).all()

        for record in records:
            # Формируем список значений для каждой записи
            values = []
            for column in columns:
                value = getattr(record, column.name)
                if column.foreign_keys:
                    # Для внешних ключей получаем строковое представление связанной записи
                    fk = list(column.foreign_keys)[0]
                    related_table = fk.column.table
                    related_model = next(m for m in table.__base__._decl_class_registry.values() if hasattr(m, '__table__') and m.__table__ == related_table)
                    related_obj = session.query(related_model).filter_by(id=value).first()
                    values.append(str(related_obj) if related_obj else "")
                else:
                    values.append(str(value) if value is not None else "")
            tree.insert("", END, values=values)

        if not records:
            messagebox.showinfo("Информация", f"Таблица {table.__tablename__} пуста")

    except SQLAlchemyError as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
    finally:
        # Закрываем сессию при закрытии окна
        modal.protocol("WM_DELETE_WINDOW", lambda: [session.close(), modal.destroy()])

    # Кнопка выхода
    Button(modal, text="Выход", command=lambda: [session.close(), modal.destroy()]).pack(anchor=NW, padx=8, pady=8)


def open_modal_window2(table, record_id=None, root=None):
    form = {}
    session = Session()  # Создаем сессию для работы с БД

    def save_record():
        data = {}
        for column in columns:
            if column.name != 'id':
                if isinstance(form[column.name]['widget'], ttk.Combobox):
                    selected_value = form[column.name]['widget'].get()
                    value = form[column.name]['widget'].related_objects.get(selected_value, None)
                    data[column.name] = value
                else:
                    value = form[column.name]['widget'].get()
                    data[column.name] = value if value != '' else None

        # Проверка обязательных полей
        for column in columns:
            if column.name != 'id' and not column.nullable and data.get(column.name) is None:
                label_text = column.comment if column.comment else column.name
                messagebox.showerror("Ошибка", f"Поле {label_text} обязательно для заполнения")
                return

        try:
            if record_id:  # Режим редактирования
                record = session.query(table).filter_by(id=record_id).first()
                if not record:
                    messagebox.showerror("Ошибка", f"Запись с ID {record_id} не найдена")
                    return
                for key, value in data.items():
                    setattr(record, key, value)
                messagebox.showinfo("Успех", "Запись успешно обновлена")
            else:  # Режим добавления
                record = table(**data)
                session.add(record)
                messagebox.showinfo("Успех", "Запись успешно добавлена")

            session.commit()
            modal.destroy()
            if root and hasattr(root, 'refresh_partners'):
                root.refresh_partners()  # Обновляем список в главном окне
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Ошибка", f"Не удалось сохранить запись: {e}")

    modal = Toplevel()
    modal.title("Редактирование записи" if record_id else "Добавление записи")
    modal.geometry("800x600")
    modal.grab_set()

    columns = table.__table__.columns
    record = None
    if record_id:
        record = session.query(table).filter_by(id=record_id).first()
        if not record:
            messagebox.showerror("Ошибка", f"Запись с ID {record_id} не найдена")
            modal.destroy()
            session.close()
            return

    for column in columns:
        if column.name != 'id':
            label_text = column.comment if column.comment else column.name
            Label(modal, text=label_text).pack(anchor=NW, padx=8)

            if column.foreign_keys:
                # Получаем связанную модель
                try:
                    fk = list(column.foreign_keys)[0]
                    related_table = fk.column.table
                    related_model = next((m for m in Base._decl_class_registry.values() if hasattr(m, '__table__') and m.__table__ == related_table), None)
                    if not related_model:
                        raise ValueError(f"Не найдена связанная модель для столбца {column.name}")

                    # Получаем все записи из связанной таблицы
                    related_objects = session.query(related_model).all()
                    if not related_objects:
                        messagebox.showwarning("Предупреждение", f"Нет записей для поля {label_text}. Поле будет отключено.")
                        cb = ttk.Combobox(modal, width=117, state="disabled")
                    else:
                        cb = ttk.Combobox(modal, width=117)
                        display_values = [str(obj) for obj in related_objects]
                        cb['values'] = display_values
                        cb.related_objects = {str(obj): obj.id for obj in related_objects}

                        # Заполняем Combobox текущим значением (для редактирования)
                        if record and getattr(record, column.name) is not None:
                            related_obj = session.query(related_model).filter_by(id=getattr(record, column.name)).first()
                            if related_obj:
                                cb.set(str(related_obj))
                        elif not record and not display_values:  # Для добавления с пустым Combobox
                            cb.set('')

                    cb.pack(anchor=NW, padx=8)
                    form[column.name] = {'widget': cb}
                except (ValueError, StopIteration) as e:
                    messagebox.showerror("Ошибка", f"Ошибка при обработке связанного поля {label_text}: {e}")
                    cb = ttk.Combobox(modal, width=117, state="disabled")
                    cb.pack(anchor=NW, padx=8)
                    form[column.name] = {'widget': cb}
            else:
                entry = Entry(modal, width=120)
                if record and getattr(record, column.name) is not None:
                    entry.insert(0, str(getattr(record, column.name)))
                entry.pack(anchor=NW, padx=8)
                form[column.name] = {'widget': entry}

    Button(modal, text="Сохранить" if record_id else "Добавить запись", command=save_record).pack(anchor=NW, padx=8, pady=8)
    Button(modal, text="Выход", command=lambda: [session.close(), modal.destroy()]).pack(anchor=NW, padx=8, pady=8)

    # Закрываем сессию при закрытии окна
    modal.protocol("WM_DELETE_WINDOW", lambda: [session.close(), modal.destroy()])
# def open_modal_window2(table, record_id=None):
#     form = {}
#     session = Session()  # Создаем сессию для работы с БД
#
#     def save_record():
#         data = {}
#         for column in columns:
#             if column.name != 'id':
#                 # Для Combobox получаем ID из related_objects
#                 if isinstance(form[column.name]['widget'], ttk.Combobox):
#                     selected_value = form[column.name]['widget'].get()
#                     data[column.name] = form[column.name]['widget'].related_objects.get(selected_value, None)
#                 else:
#                     data[column.name] = form[column.name]['widget'].get()
#
#         try:
#             if record_id:  # Режим редактирования
#                 # Загружаем существующую запись
#                 record = session.query(table).filter_by(id=record_id).first()
#                 if not record:
#                     messagebox.showerror("Ошибка", f"Запись с ID {record_id} не найдена")
#                     return
#
#                 # Обновляем поля записи
#                 for key, value in data.items():
#                     setattr(record, key, value if value != '' else None)
#                 messagebox.showinfo("Успех", "Запись успешно обновлена")
#             else:  # Режим добавления
#                 # Создаем новую запись
#                 record = table(**data)
#                 session.add(record)
#                 messagebox.showinfo("Успех", "Запись успешно добавлена")
#
#             session.commit()
#             modal.destroy()  # Закрываем окно после сохранения
#         except SQLAlchemyError as e:
#             session.rollback()
#             messagebox.showerror("Ошибка", f"Не удалось сохранить запись: {e}")
#
#     modal = Toplevel()
#     modal.title("Редактирование партнера" if record_id else "Добавление партнера")
#     modal.geometry("800x600")
#     modal.grab_set()
#
#     columns = table.__table__.columns
#     record = None
#     if record_id:
#         # Загружаем запись для редактирования
#         record = session.query(table).filter_by(id=record_id).first()
#         if not record:
#             messagebox.showerror("Ошибка", f"Запись с ID {record_id} не найдена")
#             modal.destroy()
#             return
#
#     for column in columns:
#         if column.name != 'id':
#             # Создаем метку
#             label_text = column.comment if column.comment else column.name
#             Label(modal, text=label_text).pack(anchor=NW, padx=8)
#
#             # Проверяем, является ли поле ForeignKey
#             if column.foreign_keys:
#                 # Получаем связанную модель
#                 fk = list(column.foreign_keys)[0]
#                 related_table = fk.column.table
#                 related_model = next(m for m in Base._decl_class_registry.values() if hasattr(m, '__table__') and m.__table__ == related_table)
#
#                 # Получаем все записи из связанной таблицы
#                 related_objects = session.query(related_model).all()
#
#                 # Создаем Combobox с значениями
#                 cb = ttk.Combobox(modal, width=117)
#                 display_values = [str(obj) for obj in related_objects]
#                 cb['values'] = display_values
#                 cb.related_objects = {str(obj): obj.id for obj in related_objects}
#
#                 # Заполняем Combobox текущим значением (для редактирования)
#                 if record and getattr(record, column.name):
#                     related_obj = session.query(related_model).filter_by(id=getattr(record, column.name)).first()
#                     if related_obj:
#                         cb.set(str(related_obj))
#
#                 cb.pack(anchor=NW, padx=8)
#                 form[column.name] = {'widget': cb}
#             else:
#                 # Обычное текстовое поле для не-FK полей
#                 entry = Entry(modal, width=120)
#                 # Заполняем поле текущим значением (для редактирования)
#                 if record and getattr(record, column.name) is not None:
#                     entry.insert(0, str(getattr(record, column.name)))
#                 entry.pack(anchor=NW, padx=8)
#                 form[column.name] = {'widget': entry}
#
#     Button(modal, text="Сохранить" if record_id else "Добавить запись", command=save_record).pack(anchor=NW, padx=8, pady=8)
#     Button(modal, text="Выход", command=modal.destroy).pack(anchor=NW, padx=8, pady=8)
#
#     # Закрываем сессию при закрытии окна
#     modal.protocol("WM_DELETE_WINDOW", lambda: [session.close(), modal.destroy()])
# #
# def open_modal_window(table):
#     form = {}
#     session = Session()  # Создаем сессию для работы с БД
#
#     def add_record():
#         data = {}
#         for column in columns:
#             if column.name != 'id':
#                 # Для Combobox берем значение, а не текст
#                 if isinstance(form[column.name]['widget'], ttk.Combobox):
#                     data[column.name] = form[column.name]['widget'].get()
#                 else:
#                     data[column.name] = form[column.name]['widget'].get()
#
#         messagebox.showinfo("Данные", str(data))
#         # Здесь можно добавить сохранение в БД
#
#     modal = Toplevel()
#     modal.title("Модальное окно")
#     modal.geometry("800x600")
#     modal.grab_set()
#
#     columns = table.__table__.columns
#
#     for column in columns:
#         if column.name != 'id':
#             # Создаем метку
#             label_text = column.comment if column.comment else column.name
#             Label(modal, text=label_text).pack(anchor=NW, padx=8)
#
#             # Проверяем, является ли поле ForeignKey
#             if column.foreign_keys:
#                 # Получаем связанную модель
#                 fk = list(column.foreign_keys)[0]
#                 related_model = fk.column.table
#
#                 # Получаем все записи из связанной таблицы
#                 related_objects = session.query(related_model).all()
#
#                 # Создаем Combobox с значениями
#                 cb = ttk.Combobox(modal, width=117)
#
#                 # Формируем список отображаемых значений
#                 display_values = [str(obj) for obj in related_objects]
#                 cb['values'] = display_values
#
#                 # Сохраняем оригинальные объекты для сопоставления
#                 cb.related_objects = {str(obj): obj.id for obj in related_objects}
#
#                 cb.pack(anchor=NW, padx=8)
#                 form[column.name] = {'widget': cb}
#             else:
#                 # Обычное текстовое поле для не-FK полей
#                 entry = Entry(modal, width=120)
#                 entry.pack(anchor=NW, padx=8)
#                 form[column.name] = {'widget': entry}
#
#     Button(modal, text="Добавить запись", command=add_record).pack(anchor=NW, padx=8, pady=8)
#     Button(modal, text="Выход", command=modal.destroy).pack(anchor=NW, padx=8, pady=8)

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
        # messagebox.showinfo(
        #     "Выбран партнер",
        #     f"{partner_data['id']}\n"
        #     f"{partner_data['name']}\n"
        #     f"Телефон: {partner_data['phone']}\n"
        #     f"Рейтинг: {partner_data['rating']}%"
        # )
        open_modal_window2(PartnersImport, record_id=partner_data["id"])
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
