from sqlalchemy.exc import IntegrityError

from app.domains import Activity
from app.domains.activities.repository import ActivityRepository
from app.domains.activities.schemas import ActivityRead, ActivityCreate
from app.exceptions.exceptions import NotFoundError, DataIntegrityError


class ActivityService:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository


    async def get_activities(self) -> list[ActivityRead]:
        activities = await self.activity_repository.get_activities()
        return [
            ActivityRead.model_validate(activity)
            for activity in activities
        ]


    async def get_activity(self, activity_id: int) -> ActivityRead:
        activity = await self.activity_repository.get_activity(activity_id)
        if not activity:
            raise NotFoundError(entity="Activity")
        return ActivityRead.model_validate(activity)


    async def create_activity(self, activity_data: ActivityCreate) -> ActivityRead:
        activity_orm = Activity(
            name=activity_data.name,
        )
        try:
           activity = await self.activity_repository.create_activity(activity_orm)
           await self.activity_repository.session.commit()
           return ActivityRead.model_validate(activity)
        except IntegrityError as e:
            await self.activity_repository.session.rollback()
            raise DataIntegrityError(f"Could not create activity: {str(e.orig)}")


    async def delete_activity(self, activity_id: int) -> None:
        activity = await self.activity_repository.get_activity(activity_id)
        if not activity:
            raise NotFoundError(entity="Activity")
        try:
            await self.activity_repository.delete_activity(activity)
            await self.activity_repository.session.commit()
        except IntegrityError:
            await self.activity_repository.session.rollback()
            raise DataIntegrityError