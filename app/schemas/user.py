import re
from pydantic import BaseModel, field_validator
from typing import Optional


class UserBase(BaseModel):
    login: str
    password: str


class User(UserBase):
    user_id: int
    chat_id: Optional[int] = None


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
