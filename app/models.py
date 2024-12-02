# app/models.py
from sqlalchemy import Column, Integer, String, Numeric, Date, Text, DATE, ForeignKey
from sqlalchemy.orm import relationship, join
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    from_city = Column(String(50))
    to_city = Column(String(50))
    price = Column(Numeric)
    flight_date = Column(Date)
    link = Column(Text, unique=True)
    airline = Column(String(100), nullable=True)
    stops = Column(Integer, nullable=True)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(Text, primary_key=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=True)

    cards = relationship("Card", secondary="user_cards", back_populates="users")


class Card(Base):
    __tablename__ = 'cards'

    card_id = Column(Integer, primary_key=True, autoincrement=True)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    flight_date = Column(Date, nullable=False)
    price_threshold = Column(Integer, default=-1)

    users = relationship("User", secondary="user_cards", back_populates="cards")


class UserCard(Base):  # Связующая/ассоциативная таблица
    __tablename__ = 'user_cards'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    card_id = Column(Integer, ForeignKey('cards.card_id'), primary_key=True)
