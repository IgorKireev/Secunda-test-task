from collections.abc import Sequence
from sqlalchemy.exc import IntegrityError
from app.domains.activities.models import Activity
from app.domains.activities.repository import ActivityRepository
from app.dtos import ActivityRelDTO
from app.core.exceptions import NotFoundError, DataIntegrityError
from app.domains.activities.schemas import ActivityCreate
from app.domains.organizations.schemas import OrganizationDTO


class ActivityService:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository

    async def get_activities(self) -> list[ActivityRelDTO]:
        activities = await self.activity_repository.get_activities()
        return [ActivityRelDTO.model_validate(activity) for activity in activities]

    async def get_activity(
        self, activity_id: int, organizations: bool = False
    ) -> ActivityRelDTO | list[OrganizationDTO]:
        activity = await self.activity_repository.get_activity(activity_id)
        if not activity:
            raise NotFoundError(entity="Activity")
        if organizations:
            return ActivityRelDTO.model_validate(activity).organizations
        return ActivityRelDTO.model_validate(activity)

    async def create_activity(self, activity_data: ActivityCreate) -> ActivityRelDTO:
        activity_orm = Activity(
            name=activity_data.name,
        )
        try:
            activity = await self.activity_repository.create_activity(activity_orm)
            activity_id = activity.id
            await self.activity_repository.commit()
            reloaded_activity = await self.activity_repository.get_activity(activity_id)
            return ActivityRelDTO.model_validate(reloaded_activity)
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

    async def get_activities_by_ids(
        self, activities_ids: list[int]
    ) -> Sequence[Activity]:
        activities = await self.activity_repository.get_activities_by_ids(
            activities_ids
        )
        if not activities:
            raise NotFoundError(entity="Activity")
        return activities
