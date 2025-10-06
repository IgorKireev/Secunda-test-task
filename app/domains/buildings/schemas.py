from pydantic import BaseModel, field_validator, condecimal, Field
import regex


class Address(BaseModel):
    address: str = Field(min_length=5, max_length=200)

    @classmethod
    @field_validator('address')
    def validate_address(cls, v: str) -> str:
        if not regex.match(r"^[\p{L}\d\s\.,\-]+$", v):
            raise ValueError(f"Invalid address: {v}")
        return v.strip()


class Coordinates(BaseModel):
    latitude: condecimal(ge=-90, le=90)
    longitude: condecimal(ge=-180, le=180)
