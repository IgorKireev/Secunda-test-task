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

@router.get("/{organization_id}")
async def get_organization(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ],
        organization_id: int
    ):
    return await organization_service.get_organization(organization_id)

@router.post("/")
async def create_organization(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ],
        organization_data: OrganizationCreate
    ):
    return await organization_service.create_organization(organization_data)

@router.delete("/")
async def delete_organization(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ],
        organization_id: int
    ):
    return await organization_service.delete_organization(organization_id)