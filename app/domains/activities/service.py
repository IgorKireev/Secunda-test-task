from sqlalchemy.exc import IntegrityError

from app.domains import Activity
from app.domains.activities.repository import ActivityRepository
from app.domains.activities.schemas import ActivityDTO, ActivityRelDTO, ActivityCreate
from app.exceptions.exceptions import NotFoundError, DataIntegrityError


class ActivityService:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository


    async def get_activities(self) -> list[ActivityRelDTO]:
        activities = await self.activity_repository.get_activities()
        return [
            ActivityRelDTO.model_validate(activity)
            for activity in activities
        ]


    async def get_activity(self, activity_id: int) -> ActivityRelDTO:
        activity = await self.activity_repository.get_activity(activity_id)
        if not activity:
            raise NotFoundError(entity="Activity")
        return ActivityRelDTO.model_validate(activity)


    async def create_activity(self, activity_data: ActivityCreate) -> ActivityRelDTO:
        activity_orm = Activity(
            name=activity_data.name,
        )
        try:
           activity = await self.activity_repository.create_activity(activity_orm)
           await self.activity_repository.commit()
           return ActivityRelDTO.model_validate(activity)
        except IntegrityError as e:
            await self.activity_repository.rollback()
            raise DataIntegrityError(f"Could not create activity: {str(e.orig)}")


    async def delete_activity(self, activity_id: int) -> None:
        activity = await self.activity_repository.get_activity(activity_id)
        if not activity:
            raise NotFoundError(entity="Activity")
        try:
            await self.activity_repository.delete_activity(activity)
            await self.activity_repository.commit()
        except IntegrityError:
            await self.activity_repository.rollback()
            raise DataIntegrityError

    async def get_activities_by_ids(self, activities_ids: list[int]) -> list[ActivityDTO]:
        activities = await self.activity_repository.get_activities_by_ids(activities_ids)
        if not activities:
            raise NotFoundError(entity="Activity")
        return [
            ActivityDTO.model_validate(activity)
            for activity in activities
        ]