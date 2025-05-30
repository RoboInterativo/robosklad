from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

#Сотрудники: ФИО, дата рождения, паспортные данные,
#банковские реквизиты, наличие семьи, состояние здоровья.

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(DateTime)
    passport_data = Column(String(50))
    bank_details = Column(String(100))
    has_family = Column(Boolean)
    health_status = Column(String(200))
    contact_phone = Column(String(20))
    email = Column(String(50))

# Создание базы данных
engine = create_engine('sqlite:///master_pol.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
