import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from db import Base, PartnersImport, ProductsImport, PartnerProductsImport, Session  # Импортируем ваши модели

def load_partner_products_from_excel(file_path):
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
            # Получаем данные из строки
            product_name = row['Продукция']
            partner_name = row['Наименование партнера']
            quantity = row['Количество продукции']
            sale_date = row['Дата продажи']

            # Преобразуем дату из Timestamp в объект date
            if isinstance(sale_date, pd.Timestamp):
                sale_date = sale_date.date()
            else:
                print(f"Неверный формат даты для строки {row}: {sale_date}")
                continue

            # Проверяем, существует ли партнер по company_name
            partner = session.query(PartnersImport).filter_by(company_name=partner_name).first()
            if not partner:
                print(f"Партнер {partner_name} не найден, создаем нового.")
                partner = PartnersImport(
                    company_name=partner_name,
                    inn=f"INN_{partner_name}_{hash(partner_name) % 1000000}",  # Уникальный ИНН
                    rating=0  # Минимальное значение рейтинга
                )
                session.add(partner)
                session.flush()  # Получаем partner.id без коммита

            # Проверяем, существует ли продукт по name
            product = session.query(ProductsImport).filter_by(name=product_name).first()
            if not product:
                print(f"Продукт {product_name} не найден, создаем новый.")
                product = ProductsImport(
                    name=product_name,
                    article=f"ART_{product_name}_{hash(product_name) % 1000000}",  # Уникальный артикул
                    min_partner_price=0.00  # Минимальная цена по умолчанию
                    # Если product_type_id и material_type_id обязательны, укажите значения по умолчанию, например:
                    # product_type_id=1,
                    # material_type_id=1
                )
                session.add(product)
                session.flush()  # Получаем product.id без коммита

            # Проверяем, существует ли запись в PartnerProductsImport
            existing_record = session.query(PartnerProductsImport).filter_by(
                product_id=product.id,
                partner_id=partner.id,
                sale_date=sale_date
            ).first()

            if existing_record:
                print(f"Запись для продукта {product_name} и партнера {partner_name} на дату {sale_date} уже существует. Пропускаем.")
                continue

            # Создаем новую запись в PartnerProductsImport
            new_partner_product = PartnerProductsImport(
                product_id=product.id,
                partner_id=partner.id,
                quantity=quantity,
                sale_date=sale_date
            )
            session.add(new_partner_product)
            print(f"Добавлена запись: {product_name}, {partner_name}, {quantity}, {sale_date}")

        session.commit()
        print(f"Успешно загружено {len(df)} записей в таблицу PartnerProductsImport.")

    except Exception as e:
        session.rollback()
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Укажите путь к вашему Excel файлу
    excel_file_path = "src\\static\\Partner_Products_import.xlsx"
    load_partner_products_from_excel(excel_file_path)
