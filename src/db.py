from sqlalchemy import create_engine, Boolean, DateTime, Column, Integer, String, Float, Numeric, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date

Base = declarative_base()

# ==================== Сотрудники и доступ ====================
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False, comment="ФИО сотрудника")
    birth_date = Column(DateTime, comment="Дата рождения")
    passport_data = Column(String(50), comment="Паспортные данные")
    bank_details = Column(String(100), comment="Банковские данные")
    has_family = Column(Boolean, comment="Семейное положение")
    health_status = Column(String(200), comment="Состояние здоровья")
    contact_phone = Column(String(20), comment="Контактный телефон")
    email = Column(String(50), comment="Электронная почта")

class MaterialTypeImport(Base):
    __tablename__ = 'material_type_import'
    id = Column(Integer, primary_key=True)
    type_material = Column(String(50), nullable=False, unique=True)
    procent_brack = Column(Numeric(5, 2), nullable=False)
    products = relationship("ProductsImport", back_populates="material_type")
    def __str__(self):
        return self.type_material or f"Type {self.id}"


class PartnersImport(Base):
    __tablename__ = 'partners_import'
    id = Column(Integer, primary_key=True)
    partner_type = Column(String(50))
    company_name = Column(String(100), nullable=False, unique=True)
    legal_address = Column(String(200))
    inn = Column(String(12), unique=True)
    director_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(50))
    logo_path = Column(String(200))
    rating = Column(Integer, CheckConstraint('rating >= 0'))
    partner_products = relationship("PartnerProductsImport", back_populates="partner")
    def __str__(self):
        return f"{self.partner_type} {self.company_name}" or f"Type {self.id}"


class ProductTypeImport(Base):
    __tablename__ = 'product_type_import'
    id = Column(Integer, primary_key=True)
    product_type = Column(String(100), nullable=False, unique=True)
    type_coefficient = Column(Numeric(5, 2), nullable=False)
    products = relationship("ProductsImport", back_populates="product_type")

    def __str__(self):
        return self.product_type or f"Type {self.id}"

class ProductsImport(Base):
    __tablename__ = 'products_import'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, comment="Наименование")
    article = Column(String(50), unique=True, nullable=False)
    min_partner_price = Column(Numeric(10, 2))
    product_type_id = Column(Integer, ForeignKey('product_type_import.id'), comment="Тип продукции")
    product_type = relationship("ProductTypeImport", back_populates="products")
    material_type_id = Column(Integer, ForeignKey('material_type_import.id'), comment="Тип материала")
    material_type = relationship("MaterialTypeImport", back_populates="products")
    partner_products = relationship("PartnerProductsImport", back_populates="product")
    def __str__(self):
        return self.name or f"Type {self.id}"
# Updated PartnerProductsImport model
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
