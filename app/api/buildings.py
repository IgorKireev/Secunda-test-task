from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.dependencies import get_building_service
from app.dtos import BuildingRelDTO
from app.domains.buildings.schemas import BuildingCreate
from app.domains.buildings.service import BuildingService

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get(
    "/",
    response_model=list[BuildingRelDTO],
    status_code=status.HTTP_200_OK,
    summary="Получить все здания",
    description="Возвращает список всех зданий",
)
async def get_buildings(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ]
    ):
    return await building_service.get_buildings()


@router.get(
    "/{building_id}",
    response_model=BuildingRelDTO,
    status_code=status.HTTP_200_OK,
    summary="Получить здание по ID",
    description="Возвращает информацию о конкретном здании",
)
async def get_building(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ],
        building_id: int,
    ):
    return await building_service.get_building(building_id)

@router.post(
    "/",
    response_model=BuildingRelDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое здание",
    description="Создает новое здание",
)
async def create_building(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ],
        building_data: BuildingCreate,
    ):
    return await building_service.create_building(building_data)


@router.delete(
    "/{building_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить здание",
    description="Удаляет здание из системы",
)
async def delete_building(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ],
        building_id: int,
    ):
    return await building_service.delete_building(building_id)
