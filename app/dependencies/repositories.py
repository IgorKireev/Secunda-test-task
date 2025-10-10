from app.dependencies.factories import repository_factory
from app.domains import (
    ActivityRepository,
    BuildingRepository,
    OrganizationRepository,
)

get_activity_repository = repository_factory(ActivityRepository)
get_organization_repository = repository_factory(OrganizationRepository)
get_building_repository = repository_factory(BuildingRepository)
