from app.domains import (
    ActivityDTO,
    BuildingDTO,
    OrganizationDTO,
)


class OrganizationRelDTO(OrganizationDTO):
    building: BuildingDTO
    activities: list[ActivityDTO]

class ActivityRelDTO(ActivityDTO):
    organizations: list[OrganizationDTO]

class BuildingRelDTO(BuildingDTO):
    organizations: list[OrganizationDTO]
