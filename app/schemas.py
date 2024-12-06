import re
from pydantic import BaseModel, field_validator
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


class UserBase(BaseModel):
    login: str
    password: str


class User(UserBase):
    user_id: int
    chat_id: int = None


class UserCreate(UserBase):
    @field_validator("login")
    def validate_login(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError("Логин должен содержать минимум 3 символа")
        if not re.fullmatch(r"[a-zA-Z0-9]+", value):
            raise ValueError("Логин может содержать только английские буквы и цифры")
        return value

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Пароль должен быть длиной минимум 8 символов")
        if not re.fullmatch(r"[a-zA-Z0-9]+", value):
            raise ValueError("Пароль может содержать только английские буквы и цифры")
        return value


class CityCode(BaseModel):
    code: str

    @field_validator('code')
    def validate_airport_code(cls, value: str) -> str:
        if len(value) != 3 or not re.fullmatch(r"^[A-Z]{3}$", value):
            raise ValueError("Код города неверный")
        return value


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
