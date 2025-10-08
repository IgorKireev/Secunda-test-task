from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains import Building
from app.domains.buildings.schemas import BuildingCreate, Coordinates


class BuildingRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_building(self, building_data: BuildingCreate) -> Building:
        building = Building(
            address=building_data.address,
            latitude=Coordinates(latitude=building_data.latitude),
            longitude=Coordinates(longitude=building_data.longitude),
        )
        self.session.add(building)
        await self.session.commit()
        await self.session.refresh(building)
        return building