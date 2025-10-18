from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import (
    get_organization_service,
    get_building_service,
    get_activity_service,
)
from app.domains import (
    ActivityService,
    BuildingService,
    OrganizationService,
)
from app.dependencies.auth import role_required


router = APIRouter(
    prefix="/api/v1",
    tags=["API"],
    dependencies=[Depends(role_required(["admin", "moderator", "user"]))],
)


@router.get("/buildings/building_id/organizations")
async def get_organizations_by_building(
    building_service: Annotated[BuildingService, Depends(get_building_service)],
    building_id: int,
):
    return await building_service.get_building(building_id, organizations=True)


@router.get("/activities/{activity_id}/organizations")
async def get_organizations_by_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity_id: int,
):
    return await activity_service.get_activity(activity_id, organizations=True)


@router.get("/organizations/search/title")
async def get_organization_by_title(
    organization_service: Annotated[
        OrganizationService, Depends(get_organization_service)
    ],
    title: str,
):
    return await organization_service.get_organization_by_title(title)
