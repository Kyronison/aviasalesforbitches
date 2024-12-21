# user.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base  # Импортируем общий Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(Text, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=True, default=None)

    cards = relationship("Card", back_populates="user", cascade="all, delete-orphan")