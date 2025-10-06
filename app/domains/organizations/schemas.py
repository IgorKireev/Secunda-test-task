from pydantic import BaseModel, field_validator, Field
import phonenumbers
from app.domains.buildings import BuildingBase


class PhoneNumber(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def validate_number(cls, v: str) -> str:
        parsed = phonenumbers.parse(v, None)
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError(f"Invalid phone number: {v}")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)


class Organizations(BaseModel):
    title: str
    phone_numbers: list[PhoneNumber] = Field(default_factory=list)
    building: BuildingBase


    @classmethod
    @field_validator('phone_numbers', mode='before')
    def ensure_phone_objects(cls, v: str | PhoneNumber | list[str | PhoneNumber]):
        if isinstance(v, PhoneNumber):
            return [v]
        elif isinstance(v, str):
            return [PhoneNumber(phone_number=v)]
        elif isinstance(v, list):
            return [
                PhoneNumber(phone_number=p) if isinstance(p, str) else p
                for p in v
            ]
        return v
