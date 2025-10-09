from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.domains import Building


class BuildingRepository():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get_buildings(self) -> Sequence[Building]:
        query = (
            select(Building)
            .options(selectinload(Building.organization))
        )
        buildings = await self.session.execute(query)
        return buildings.scalars().all()


    async def get_building(self, building_id) -> Building | None:
        query = (
            select(Building)
            .filter(Building.id == building_id)
            .options(selectinload(Building.organization))
        )
        building = await self.session.execute(query)
        return building.scalar_one_or_none()


    async def create_building(self, building: Building) -> Building:
        self.session.add(building)
        await self.session.commit()
        await self.session.refresh(building)
        return building


    async def delete_building(self, building: Building) -> None:
        await self.session.delete(building)
        await self.session.commit()