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
        if not re.fullmatch(r"[a-zA-Z]+", value):
            raise ValueError("Логин может содержать только английские буквы и цифры")
        return value

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Пароль должен быть длиной минимум 8 символов")
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(char.isupper() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.fullmatch(r"[a-zA-Z0-9]+", value):
            raise ValueError("Пароль может содержать только английские буквы и цифры")
        return value
