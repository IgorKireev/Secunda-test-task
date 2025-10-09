from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.domains import Activity


class ActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get_activities(self) -> Sequence[Activity]:
        query = (
            select(Activity)
            .options(selectinload(Activity.organizations))
        )
        activities = await self.session.execute(query)
        return activities.scalars().all()


    async def get_activity(self, activity_id: int) -> Activity | None:
        query = (
            select(Activity)
            .filter(Activity.id == activity_id)
            .options(selectinload(Activity.organizations))
        )
        activity = await self.session.execute(query)
        return activity.scalar_one_or_none()


    async def create_activity(self, activity: Activity) -> Activity:
        self.session.add(activity)
        await self.session.flush()
        return activity


    async def delete_activity(self, activity: Activity) -> None:
        await self.session.delete(activity)
