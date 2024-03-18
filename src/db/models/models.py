from sqlalchemy import Column, Integer, String, Text
from src.db.base import Base
from datetime import datetime
from sqlalchemy import DateTime


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = {"comment": "Книга контактов"}

    id = Column(Integer, primary_key=True, comment="Уникальный идентификатор")
    name = Column(String, nullable=False, comment="Имя контакта")
    discription = Column(Text, comment="Описание контаката")
    created_at = Column(DateTime, comment="Дата создания", default=datetime.now)
    updated_at = Column(
        DateTime, comment="Дата обновления", default=datetime.now, onupdate=datetime.now
    )
