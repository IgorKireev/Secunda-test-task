from pydantic import BaseModel, Field, ConfigDict


class ActivityBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)


class ActivityCreate(ActivityBase):
    pass


class ActivityDTO(ActivityBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )
