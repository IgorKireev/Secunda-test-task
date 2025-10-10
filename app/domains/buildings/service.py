from sqlalchemy.exc import IntegrityError
from app.domains.buildings.models import Building
from app.domains.buildings.repository import BuildingRepository
from app.dtos import BuildingRelDTO
from app.exceptions.exceptions import NotFoundError, DataIntegrityError
from app.domains.buildings.schemas import BuildingCreate
from app.domains.organizations.schemas import OrganizationDTO


class BuildingService:
    def __init__(self, building_repository: BuildingRepository) -> None:
        self.building_repository = building_repository


    async def get_buildings(self) -> list[BuildingRelDTO]:
        buildings = await self.building_repository.get_buildings()
        return [
            BuildingRelDTO.model_validate(building)
            for building in buildings
        ]


    async def get_building(self, building_id: int, organizations: bool = False) -> BuildingRelDTO | list[OrganizationDTO]:
        building = await self.building_repository.get_building(building_id)
        if not building:
            raise NotFoundError(entity="Building")
        if organizations:
            return BuildingRelDTO.model_validate(building).organizations
        return BuildingRelDTO.model_validate(building)


    async def create_building(self, building_data: BuildingCreate) -> BuildingRelDTO:
        building_orm = Building(
            address=building_data.address,
            latitude=building_data.latitude,
            longitude=building_data.longitude,
        )
        try:
            building = await self.building_repository.create_building(building_orm)
            building_id = building.id
            await self.building_repository.commit()
            reloaded_building = await self.building_repository.get_building(building_id)
            return BuildingRelDTO.model_validate(reloaded_building)
        except IntegrityError as e:
            await self.building_repository.rollback()
            raise DataIntegrityError(f"Could not create building: {str(e.orig)}")


    async def delete_building(self, building_id: int) -> None:
        building = await self.building_repository.get_building(building_id)
        if not building:
            raise NotFoundError(entity="Building")
        try:
            await self.building_repository.delete_building(building)
            await self.building_repository.commit()
        except IntegrityError:
            await self.building_repository.rollback()
            raise DataIntegrityError