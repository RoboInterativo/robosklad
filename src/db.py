from sqlalchemy import create_engine, Boolean,DateTime, Column, Integer, String, Float, Numeric, ForeignKey, Date,CheckConstraint
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date

Base = declarative_base()
# ==================== Сотрудники и доступ ====================
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False,comment="ФИО сотрудника")
    birth_date = Column(DateTime,comment="Дата рождения")
    passport_data = Column(String(50),comment="Паспортные данные")
    bank_details = Column(String(100), comment="Банковские данные")
    has_family = Column(Boolean, comment="ФИО сотрудника")
    health_status = Column(String(200), comment="ФИО сотрудника")
    contact_phone = Column(String(20),comment="ФИО сотрудника")
    email = Column(String(50), comment="ФИО сотрудника")


class MaterialTypeImport(Base):
    __tablename__ = 'material_type_import'
    id = Column(Integer, primary_key=True)
    type_material = Column(String(50), nullable=False, unique=True)
    procent_brack = Column(Numeric(5, 2), nullable=False)  # Процент брака (например, 0.05 для 5%)
    products = relationship("ProductsImport", back_populates="material_type")

class ProductTypeImport(Base):
    __tablename__ = 'product_type_import'
    id = Column(Integer, primary_key=True)
    product_type = Column(String(100), nullable=False, unique=True)
    type_coefficient = Column(Numeric(5, 2), nullable=False)  # Коэффициент типа продукции
    products = relationship("ProductsImport", back_populates="product_type")

class PartnersImport(Base):
    __tablename__ = 'partners_import'
    id = Column(Integer, primary_key=True)
    partner_type = Column(String(50))  # Например, "ЗАО", "ООО"
    company_name = Column(String(100), nullable=False, unique=True)
    legal_address = Column(String(200))
    inn = Column(String(12), unique=True)
    director_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(50))
    logo_path = Column(String(200))
    rating = Column(Integer, CheckConstraint('rating >= 0'))  # Рейтинг неотрицательный
    partner_products = relationship("PartnerProductsImport", back_populates="partner")

class ProductsImport(Base):
    __tablename__ = 'products_import'
    id = Column(Integer, primary_key=True)
    article = Column(String(50), unique=True, nullable=False)
    product_type_id = Column(Integer, ForeignKey('product_type_import.id'), nullable=False)
    material_type_id = Column(Integer, ForeignKey('material_type_import.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    image_path = Column(String(200))
    min_partner_price = Column(Numeric(10, 2))  # Используем Numeric для точности
    package_length = Column(Numeric(10, 2))  # Длина упаковки
    package_width = Column(Numeric(10, 2))  # Ширина упаковки
    package_height = Column(Numeric(10, 2))  # Высота упаковки
    net_weight = Column(Numeric(10, 2))
    gross_weight = Column(Numeric(10, 2))
    quality_certificate_path = Column(String(200))
    standard_number = Column(String(50))
    production_time = Column(Integer)
    cost_price = Column(Numeric(10, 2))
    workshop_number = Column(Integer)
    required_workers = Column(Integer)
    product_type = relationship("ProductTypeImport", back_populates="products")
    material_type = relationship("MaterialTypeImport", back_populates="products")
    partner_products = relationship("PartnerProductsImport", back_populates="product")

class PartnerProductsImport(Base):
    __tablename__ = 'partner_products_import'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products_import.id'), nullable=False)
    partner_id = Column(Integer, ForeignKey('partners_import.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    product = relationship("ProductsImport", back_populates="partner_products")
    partner = relationship("PartnersImport", back_populates="partner_products")

# Создание базы данных
engine = create_engine('sqlite:///master_pol.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
