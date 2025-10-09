from app.domains.activities.repository import ActivityRepository
from app.domains.activities.schemas import ActivityRead, ActivityCreate


class ActivityService:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository


    async def get_activities(self) -> list[ActivityRead]:
        activities_orm = await self.activity_repository.get_activities()
        return [
            ActivityRead.model_validate(activity)
            for activity in activities_orm
        ]