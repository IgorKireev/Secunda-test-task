from pydantic import BaseModel, field_validator, Field, ConfigDict
import phonenumbers
from app.domains.activities import ActivityBase
from app.domains.buildings import BuildingBase


class PhoneNumber(BaseModel):
    phone_number: str

    @classmethod
    @field_validator('phone_number')
    def validate_number(cls, v: str) -> str:
        parsed = phonenumbers.parse(v, None)
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError(f"Invalid phone number: {v}")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)


class OrganizationBase(BaseModel):
    title: str = Field(max_length=30)
    phone_numbers: list[PhoneNumber] = Field(default_factory=list)

    @classmethod
    @field_validator('phone_numbers', mode='before')
    def ensure_phone_objects(cls, v: str | PhoneNumber | list[str | PhoneNumber]):
        if not v:
            return []
        if isinstance(v, (str, PhoneNumber)):
            v = [v]
        return [
            PhoneNumber(phone_number=p) if isinstance(p, str) else p
            for p in v
        ]


class OrganizationCreate(OrganizationBase):
    building_id: int = Field(...)
    activity_ids: list[int] = Field(default_factory=list)


class OrganizationRead(OrganizationBase):
    id: int
    building: BuildingBase
    activities: list[ActivityBase]

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )