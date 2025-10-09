from app.domains.activities.repository import ActivityRepository
from app.domains.activities.schemas import ActivityRead, ActivityCreate
from app.exceptions.exceptions import NotFoundError


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