from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.dependencies import get_organization_service
from app.dtos import OrganizationRelDTO
from app.domains.organizations.schemas import OrganizationCreate
from app.domains.organizations.service import OrganizationService


router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get(
    "/",
    response_model=list[OrganizationRelDTO],
    status_code=status.HTTP_200_OK,
    summary="Получить все организации",
    description="Возвращает список всех организаций",
)
async def get_organizations(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ]
    ):
    return await organization_service.get_organizations()

@router.get(
    "/{organization_id}",
    response_model=OrganizationRelDTO,
    status_code=status.HTTP_200_OK,
    summary="Получить организацию по ID",
    description="Возвращает информацию о конкретной организации",
)
async def get_organization(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ],
        organization_id: int
    ):
    return await organization_service.get_organization(organization_id)

@router.post(
    "/",
    response_model=OrganizationRelDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую организацию",
    description="Создает новую организацию",
)
async def create_organization(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ],
        organization_data: OrganizationCreate
    ):
    return await organization_service.create_organization(organization_data)

@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить организацию",
    description="Удаляет организацию из системы",
)
async def delete_organization(
        organization_service: Annotated[
            OrganizationService,
            Depends(get_organization_service)
        ],
        organization_id: int
    ):
    return await organization_service.delete_organization(organization_id)