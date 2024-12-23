from sqlalchemy import Column, Integer, String, Numeric, Date, Text
from .base import Base  # Импортируем общий Base

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


