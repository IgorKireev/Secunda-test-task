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


class BuildingBase(BaseModel):
    address: Address
    coordinates: Coordinates

    @classmethod
    @field_validator('coordinates')
    def validate_coordinates_meaningful(cls, v: Coordinates) -> Coordinates:
        if v.latitude == 0 and v.longitude == 0:
            raise ValueError("Coordinates cannot be exactly (0, 0)")
        return v


class BuildingCreate(BuildingBase):
    pass

class BuildingRead(BuildingBase):
    id: int

    class Config:
        from_attributes = True