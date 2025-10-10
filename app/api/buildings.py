from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import get_building_service
from app.domains.buildings.schemas import BuildingCreate
from app.domains.buildings.service import BuildingService

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/")
async def get_buildings(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ]
    ):
    return await building_service.get_buildings()


@router.get("/{building_id}")
async def get_building(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ],
        building_id: int,
    ):
    return await building_service.get_building(building_id)

@router.post("/")
async def create_building(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ],
        building_data: BuildingCreate,
    ):
    return await building_service.create_building(building_data)


@router.delete("/")
async def delete_building(
        building_service: Annotated[
            BuildingService,
            Depends(get_building_service)
        ],
        building_id: int,
    ):
    return await building_service.delete_building(building_id)
