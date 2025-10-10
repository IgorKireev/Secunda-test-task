from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.domains.activities.models import Activity
from app.domains.organizations.models import Organization


class ActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get_activities(self) -> Sequence[Activity]:
        query = (
            select(Activity)
            .options(
                selectinload(Activity.organizations)
                .selectinload(Organization.phone_numbers),
            )
        )
        activities = await self.session.execute(query)
        return activities.scalars().all()


    async def get_activity(self, activity_id: int) -> Activity | None:
        query = (
            select(Activity)
            .filter(Activity.id == activity_id)
            .options(
                selectinload(Activity.organizations)
                .selectinload(Organization.phone_numbers),
            )
        )
        activity = await self.session.execute(query)
        return activity.scalar_one_or_none()


    async def create_activity(self, activity: Activity) -> Activity:
        self.session.add(activity)
        await self.session.flush()
        return activity


    async def delete_activity(self, activity: Activity) -> None:
        await self.session.delete(activity)

    async def get_activities_by_ids(self, activities_ids: list[int]) -> Sequence[Activity]:
        query = (
            select(Activity)
            .filter(
                Activity.id.in_(activities_ids)
            )
        )
        activities = await self.session.execute(query)
        return activities.scalars().all()


    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()