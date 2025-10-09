from sqlalchemy.exc import IntegrityError
from app.domains import Building
from app.domains.buildings.repository import BuildingRepository
from app.domains.buildings.schemas import BuildingRead, BuildingCreate
from app.exceptions.exceptions import NotFoundError, DataIntegrityError


class BuildingService:
    def __init__(self, building_repository: BuildingRepository) -> None:
        self.building_repository = building_repository


    async def get_buildings(self) -> list[BuildingRead]:
        buildings_orm = await self.building_repository.get_buildings()
        return [
            BuildingRead.model_validate(building)
            for building in buildings_orm
        ]


    async def get_building(self, building_id: int) -> BuildingRead:
        building = await self.building_repository.get_building(building_id)
        if not building:
            raise NotFoundError(entity="Building")
        return BuildingRead.model_validate(building)


    async def create_building(self, building_data: BuildingCreate) -> BuildingRead:
        building_orm = Building(
            address=building_data.address,
            latitude=building_data.latitude,
            longitude=building_data.longitude,
        )
        try:
            building = await self.building_repository.create_building(building_orm)
            await self.building_repository.session.commit()
            return BuildingRead.model_validate(building)
        except IntegrityError as e:
            await self.building_repository.session.rollback()
            raise DataIntegrityError(f"Could not create building: {str(e.orig)}")


    async def delete_building(self, building_id: int) -> None:
        building = await self.building_repository.get_building(building_id)
        if not building:
            raise NotFoundError(entity="Building")
        try:
            await self.building_repository.delete_building(building)
            await self.building_repository.session.commit()
        except IntegrityError:
            await self.building_repository.session.rollback()
            raise DataIntegrityError