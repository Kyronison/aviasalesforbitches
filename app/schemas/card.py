from pydantic import BaseModel
from datetime import date
from typing import Optional
from .city_code import CityCode


class CardBase(BaseModel):
    origin: CityCode
    destination: CityCode
    flight_date: date
    price_threshold: Optional[int] = None


class Card(CardBase):
    card_id: int

    class Config:
        from_attributes = True


class CardCreate(CardBase):
    user_login: str
