def open_modal_window():
    modal = Toplevel()
    modal.title("Модальное окно")
    modal.geometry("800x600")
    modal.grab_set()
    columns = Employee.__table__.columns
    form={}
    for column in columns:
        field={}
        if column.name !='id':
            desk= column.comment  if column.comment else  column.comment
            field['label']= Label(modal, text=desk)
            field['label'].pack(anchor=NW )
            field['entry']= Entry(modal)
            field['entry'].pack(anchor=NW)
            form[column.name]=field

    btn_close = Button(modal, text="OK", command=modal.destroy)
    btn_close.pack(anchor=NW, padx=8, pady=8)


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
Button(frame_buttons, text="О
