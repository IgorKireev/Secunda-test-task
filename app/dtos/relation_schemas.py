from app.domains.activities.schemas import ActivityDTO
from app.domains.buildings.schemas import BuildingDTO
from app.domains.organizations.schemas import OrganizationDTO


class OrganizationRelDTO(OrganizationDTO):
    building: BuildingDTO
    activities: list[ActivityDTO]

class ActivityRelDTO(ActivityDTO):
    organizations: list[OrganizationDTO]

class BuildingRelDTO(BuildingDTO):
    organizations: list[OrganizationDTO]
