import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db import Base, PartnersImport, Session  # Импортируем ваши модели

def load_partners_from_excel(file_path):
    # Чтение Excel файла
    try:
        df = pd.read_excel(file_path)
        print("Файл успешно прочитан:")
        print(df.head())
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Создаем сессию
    session = Session()

    try:
        for _, row in df.iterrows():
            # Проверяем, существует ли партнер с таким ИНН
            existing_partner = session.query(PartnersImport)\
                                   .filter_by(inn=str(row['ИНН']))\
                                   .first()

            if existing_partner:
                print(f"Партнер с ИНН {row['ИНН']} уже существует. Пропускаем.")
                continue

            # Создаем нового партнера
            new_partner = PartnersImport(
                partner_type=row['Тип партнера'],
                company_name=row['Наименование партнера'],
                director_name=row['Директор'],
                email=row['Электронная почта партнера'],
                phone=row['Телефон партнера'],
                legal_address=row['Юридический адрес партнера'],
                inn=str(row['ИНН']),
                rating=row['Рейтинг'],
                # Для полей, которых нет в Excel, можно установить значения по умолчанию
                logo_path=None  # Можно добавить путь к логотипу позже
            )

            session.add(new_partner)

        session.commit()
        print(f"Успешно загружено {len(df)} партнеров в базу данных.")

    except Exception as e:
        session.rollback()
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Укажите путь к вашему Excel файлу
    excel_file_path = "src\static\Partners_import.xlsx"

    # Загрузка данных
    load_partners_from_excel(excel_file_path)
