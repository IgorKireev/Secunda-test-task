from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import get_activity_service
from app.domains.activities.schemas import ActivityCreate
from app.domains.activities.service import ActivityService


router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("/")
async def get_activity(
        activity_service: Annotated[
            ActivityService,
            Depends(get_activity_service)
        ]
    ):
    return await activity_service.get_activities()

@router.get("/{activity_id}")
async def get_activity(
        activity_service: Annotated[
            ActivityService,
            Depends(get_activity_service)
        ],
        activity_id: int
    ):
    return await activity_service.get_activity(activity_id)


@router.post("/")
async def create_activity(
        activity_service: Annotated[
            ActivityService,
            Depends(get_activity_service)
        ],
        activity_data: ActivityCreate
    ):
    return await activity_service.create_activity(activity_data)


@router.delete("/{activity_id}")
async def delete_activity(
        activity_service: Annotated[
            ActivityService,
            Depends(get_activity_service)
        ],
        activity_id: int
    ):
    return await activity_service.delete_activity(activity_id)