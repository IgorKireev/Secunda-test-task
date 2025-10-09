from pydantic import BaseModel, condecimal, Field, ConfigDict


class BuildingBase(BaseModel):
    address: str = Field(min_length=5, max_length=30)
    latitude: condecimal(ge=-90, le=90)
    longitude: condecimal(ge=-180, le=180)


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )