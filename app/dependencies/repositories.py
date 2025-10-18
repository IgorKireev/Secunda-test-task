from app.dependencies.factories import repository_factory
from app.domains import (
    ActivityRepository,
    BuildingRepository,
    OrganizationRepository,
    UserRepository,
    AuthRepository,
)


get_activity_repository = repository_factory(ActivityRepository)
get_building_repository = repository_factory(BuildingRepository)
get_organization_repository = repository_factory(OrganizationRepository)
get_user_repository = repository_factory(UserRepository)
get_auth_repository = repository_factory(AuthRepository)
