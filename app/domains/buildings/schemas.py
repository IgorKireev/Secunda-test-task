from pydantic import BaseModel, field_validator
import regex


class Address(BaseModel):
    address: str

    @field_validator('address')
    @classmethod
    def validate_address(cls, v: str) -> str:
        if not regex.match(r"^[\w\s\.-]+, \d+(/\d+)?$", v):
            raise ValueError(f"Invalid address: {v}")
        return v.strip()
