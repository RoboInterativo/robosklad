from tkinter import *
from tkinter import messagebox, ttk
from db import *
from db import Session, ProductTypeImport, Employee
from datetime import datetime
import re

def add_employee():
    session = Session()
    try:
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
        session.add(new_employee)
        session.commit()
        messagebox.showinfo("Успех", f"Сотрудник {new_employee.full_name} успешно добавлен!")
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
        messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {e}")
    finally:
        session.close()

def load_product_types(tree):
    # Очищаем таблицу
    for item in tree.get_children():
        tree.delete(item)

    # Загружаем данные из ProductTypeImport
    session = Session()
    try:
        product_types = session.query(ProductTypeImport).all()
        for pt in product_types:
            tree.insert("", END, values=(pt.product_type, pt.type_coefficient))
    except Exception as e:
        print(f"Ошибка при загрузке типов продукции: {e}")
        messagebox.showerror("Ошибка", f"Не удалось загрузить типы продукции: {e}")
    finally:
        session.close()

def add_product_type(tree):
    session = Session()

    def save_product_type():
        product_type = entry_product_type.get().strip()
        type_coefficient = entry_coefficient.get().strip()

        # Валидация данных
        if not product_type:
            messagebox.showerror("Ошибка", "Поле 'Тип продукции' не может быть пустым!")
            return
        if len(product_type) > 100:
            messagebox.showerror("Ошибка", "Тип продукции не должен превышать 100 символов!")
            return
        try:
            type_coefficient = float(type_coefficient)
            if type_coefficient <= 0:
                messagebox.showerror("Ошибка", "Коэффициент должен быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Коэффициент должен быть числом (например, 1.2)!")
            return

        try:
            # Проверяем уникальность product_type
            existing = session.query(ProductTypeImport).filter_by(product_type=product_type).first()
            if existing:
                messagebox.showerror("Ошибка", f"Тип продукции '{product_type}' уже существует!")
                return

            # Создаем новый тип продукции
            new_product_type = ProductTypeImport(
                product_type=product_type,
                type_coefficient=type_coefficient
            )

            # Добавляем и сохраняем
            session.add(new_product_type)
            session.commit()
            messagebox.showinfo("Успех", f"Тип продукции '{product_type}' успешно добавлен!")

            # Обновляем таблицу
            load_product_types(tree)
            modal.destroy()

        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")
            messagebox.showerror("Ошибка", f"Не удалось добавить тип продукции: {e}")
        finally:
            session.close()

    # Создаем модальное окно для добавления типа продукции
    modal = Toplevel()
    modal.title("Добавить тип продукции")
    modal.geometry("400x300")
    modal.grab_set()
    modal.resizable(False, False)

    # Поле для product_type
    Label(modal, text="Тип продукции:", font=("Arial", 12)).pack(anchor=NW, padx=10, pady=10)
    entry_product_type = Entry(modal, width=40)
    entry_product_type.pack(anchor=NW, padx=10, pady=5)

    # Поле для type_coefficient
    Label(modal, text="Коэффициент типа (например, 1.2):", font=("Arial", 12)).pack(anchor=NW, padx=10, pady=10)
    entry_coefficient = Entry(modal, width=40)
    entry_coefficient.pack(anchor=NW, padx=10, pady=5)

    # Кнопки
    frame_buttons = Frame(modal)
    frame_buttons.pack(anchor=NW, padx=10, pady=20)
    Button(frame_buttons, text="Сохранить", command=save_product_type, width=15).pack(side=LEFT, padx=5)
    Button(frame_buttons, text="Отмена", command=modal.destroy, width=15).pack(side=LEFT, padx=5)

def open_modal_window():
    modal = Toplevel()
    modal.title("Модальное окно")
    modal.geometry("800x600")
    modal.grab_set()

    label = Label(modal, text="ФИО")
    label.pack(anchor=NW, padx=8, pady=8)
    entry = Entry(modal)
    entry.pack(anchor=NW, padx=8, pady=8)
    btn_close = Button(modal, text="OK", command=modal.destroy)
    btn_close.pack(anchor=NW, padx=8, pady=8)

def main():
    root = Tk()
    root.title("Система управления партнёрами")
    root.geometry("800x600")

    # Пытаемся загрузить иконку
    try:
        root.iconbitmap("src/static/app.ico")
    except:
        print("Иконка не загружена!")
        messagebox.showwarning("Предупреждение", "Иконка приложения не найдена!")

    # Логотип
    try:
        logo = PhotoImage(file="src/static/logo.png")
        Label(root, image=logo).pack(anchor=NW, padx=10, pady=10)
        root.logo = logo
    except:
        print("Логотип не загружен!")
        messagebox.showwarning("Предупреждение", "Логотип не найден!")

    Label(root, text="Система управления партнёрами", font=("Arial", 14, "bold")).pack(pady=10)

    # Создаем таблицу для списка типов продукции
    tree_frame = Frame(root)
    tree_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, columns=("Product Type", "Coefficient"), show="headings")
    tree.heading("Product Type", text="Тип продукции")
    tree.heading("Coefficient", text="Коэффициент")
    tree.column("Product Type", width=400)
    tree.column("Coefficient", width=100, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)

    # Загружаем данные в таблицу
    load_product_types(tree)

    # Кнопки
    frame_buttons = Frame(root)
    frame_buttons.pack(pady=20)
    Button(frame_buttons, text="Добавить сотрудника", command=add_employee, width=20).pack(side=LEFT, padx=10)
    Button(frame_buttons, text="Добавить тип продукции", command=lambda: add_product_type(tree), width=20).pack(side=LEFT, padx=10)
    Button(frame_buttons, text="Открыть модальное окно", command=open_modal_window, width=20).pack(side=LEFT, padx=10)

    root.mainloop()

if __name__ == '__main__':
    main()
