from pydantic import BaseModel, Field, ConfigDict

from app.domains.organizations.models import Organization
from app.domains.organizations.schemas import OrganizationDTO


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

class ActivityRelDTO(ActivityDTO):
    organizations: list["OrganizationDTO"]