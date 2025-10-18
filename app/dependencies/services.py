from typing import Annotated
from fastapi import Depends
from app.dependencies.repositories import (
    get_activity_repository,
    get_building_repository,
    get_organization_repository,
    get_user_repository,
)
from app.domains import (
    ActivityRepository,
    ActivityService,
    BuildingRepository,
    BuildingService,
    OrganizationRepository,
    OrganizationService,
    UserRepository,
    UserService,
)


def get_activity_service(
        activity_repository: Annotated[
            ActivityRepository,
            Depends(get_activity_repository)
        ]
    ):
    return ActivityService(
        activity_repository=activity_repository,
    )

async def get_building_service(
        building_repository: Annotated[
            BuildingRepository,
            Depends(get_building_repository)
        ]
    ):
    return BuildingService(
        building_repository=building_repository
    )

def get_organization_service(
        organization_repository: Annotated[
            OrganizationRepository,
            Depends(get_organization_repository)
        ],
        activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    ):
    return OrganizationService(
        organization_repository=organization_repository,
        activity_service=activity_service
    )

def get_user_service(
        user_repository: Annotated[
            UserRepository,
            Depends(get_user_repository)
        ]
    ):
    return UserService(
        user_repository=user_repository
    )
