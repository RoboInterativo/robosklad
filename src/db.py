from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

#Сотрудники: ФИО, дата рождения, паспортные данные,
#банковские реквизиты, наличие семьи, состояние здоровья.

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    article = Column(String(50), unique=True)
    product_type = Column(String(50))
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    image_path = Column(String(200))
    min_partner_price = Column(Float)
    package_length = Column(Float)
    package_width = Column(Float)
    package_height = Column(Float)
    net_weight = Column(Float)
    gross_weight = Column(Float)
    quality_certificate_path = Column(String(200))
    standard_number = Column(String(50))
    production_time = Column(Integer)  # в часах
    cost_price = Column(Float)
    workshop_number = Column(Integer)
    required_workers = Column(Integer)



class Partners(Base):
    __tablename__ = 'partners'
    id = Column(Integer, primary_key=True)
    partner_type = Column(String(50))  # розница, опт, интернет-магазин и т.д.
    company_name = Column(String(100), nullable=False)
    legal_address = Column(String(200))
    inn = Column(String(12), unique=True)
    director_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(50))
    logo_path = Column(String(200))
    rating = Column(Integer)



class Type_marerial(Base):
    __tablename__ = 'Type_marerial'
    id = Column(Integer, primary_key=True)
    Type_marerial = Column(String(50))  # розница, опт, интернет-магазин и т.д.
    procent_brack = Column(Float(10), nullable=False)



class Prodaga(Base):
    __tablename__ = 'prodaga'
    id = Column(Integer, primary_key=True)
    product = Column(String(50))  # розница, опт, интернет-магазин и т.д.
    partner_name = Column(String(100), nullable=False)
    kol_tovara = Column(Integer)
    inn = Column(String(12), unique=True)
    director_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(50))
    logo_path = Column(String(200))
    rating = Column(Integer)


# Создание базы данных
engine = create_engine('sqlite:///master_pol.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
