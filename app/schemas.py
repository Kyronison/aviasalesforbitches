from pydantic import BaseModel
from datetime import date
from typing import Optional

class TicketBase(BaseModel):
    from_city: str
    to_city: str
    price: float
    flight_date: date
    link: str
    airline: Optional[str] = None
    stops: Optional[int] = 0

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int

    class Config:
        from_attributes = True