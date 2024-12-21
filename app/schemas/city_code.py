import re
from pydantic import BaseModel, field_validator


class CityCode(BaseModel):
    code: str

    @field_validator('code')
    def validate_airport_code(cls, value: str) -> str:
        if len(value) != 3 or not re.fullmatch(r"^[A-Z]{3}$", value):
            raise ValueError("Код города неверный")
        return value
