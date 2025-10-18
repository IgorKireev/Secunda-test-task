from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.dependencies import get_activity_service
from app.dependencies.auth import role_required
from app.dtos import ActivityRelDTO
from app.domains.activities.schemas import ActivityCreate
from app.domains.activities.service import ActivityService


router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
    dependencies=[Depends(role_required(["admin", "moderator"]))],
)


@router.get(
    "/",
    response_model=list[ActivityRelDTO],
    status_code=status.HTTP_200_OK,
    summary="Получить все деятельности",
    description="Возвращает список всех деятельностей",
)
async def get_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
):
    return await activity_service.get_activities()


@router.get(
    "/{activity_id}",
    response_model=ActivityRelDTO,
    status_code=status.HTTP_200_OK,
    summary="Получить деятельность по ID",
    description="Возвращает информацию о конкретной деятельности",
)
async def get_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity_id: int,
):
    return await activity_service.get_activity(activity_id)


@router.post(
    "/",
    response_model=ActivityRelDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новой деятельности",
    description="Создает новую деятельность",
)
async def create_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity_data: ActivityCreate,
):
    return await activity_service.create_activity(activity_data)


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить деятельность",
    description="Удаляет деятельность из системы",
)
async def delete_activity(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
    activity_id: int,
):
    return await activity_service.delete_activity(activity_id)
