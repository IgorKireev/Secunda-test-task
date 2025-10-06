from pydantic import BaseModel, field_validator, Field
import phonenumbers


class PhoneNumber(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def validate_number(cls, v: str) -> str:
        parsed = phonenumbers.parse(v, None)
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError(f"Invalid phone number: {v}")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)


