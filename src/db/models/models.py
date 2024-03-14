from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.db.base import Base

class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = {"comment": "Книга контактов"}

    id = Column(Integer, primary_key=True, comment="Уникальный идентификатор")
    name = Column(String, nullable=False, comment="Имя контакта")
    discription = Column(Text, comment="Описание контакат")
    created_at = Column(Date, comment="Дата создания", default="now()")
    updated_at = Column(Date, comment="Дата обновления", default="now()")
