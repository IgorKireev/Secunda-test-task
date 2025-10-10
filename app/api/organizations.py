from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import get_organization_service
from app.domains.organizations.schemas import OrganizationCreate
from app.domains.organizations.service import OrganizationService


router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/")
async def get_organizations(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ]
):
    return await organization_service.get_organizations()