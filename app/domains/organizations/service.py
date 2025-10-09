from sqlalchemy.exc import IntegrityError
from app.domains.organizations.models import Organization
from app.domains.organizations.repository import OrganizationRepository
from app.domains.organizations.schemas import OrganizationRelDTO, OrganizationCreate, PhoneNumber
from app.exceptions.exceptions import NotFoundError, DataIntegrityError
from app.domains.activities import ActivityService


class OrganizationService:
    def __init__(
            self,
            organization_repository: OrganizationRepository,
            activity_service: ActivityService
    ) -> None:
        self.organization_repository = organization_repository
        self.activity_service = activity_service

    async def get_organizations(self) -> list[OrganizationRelDTO]:
        organizations = await self.organization_repository.get_organizations()
        return [
            OrganizationRelDTO.model_validate(organization)
            for organization in organizations
        ]

    async def get_organization(self, organization_id: int) -> OrganizationRelDTO:
        organization = await self.organization_repository.get_organization(organization_id)
        if not organization:
            raise NotFoundError(entity="Organization")
        return OrganizationRelDTO.model_validate(organization)

    async def create_organization(self, organization_data: OrganizationCreate) -> OrganizationRelDTO:
        organization_orm = Organization(
            title=organization_data.title,
            building_id=organization_data.building_id,
        )
        organization_orm.phone_numbers = [
            PhoneNumber(phone_number=phone_number)
            for phone_number in organization_data.phone_numbers
        ]
        organization_orm.activities = await self.activity_service.get_activities_by_ids(
            organization_data.activity_ids
        )
        try:
            organization = await self.organization_repository.create_organization(organization_orm)
            await self.organization_repository.commit()
            return OrganizationRelDTO.model_validate(organization)
        except IntegrityError as e:
            await self.organization_repository.rollback()
            raise DataIntegrityError(f"Could not create organization: {str(e.orig)}")


    async def delete_organization(self, organization_id: int) -> None:
        organization = await self.organization_repository.get_organization(organization_id)
        if not organization:
            raise NotFoundError(entity="Organization")
        try:
            await self.organization_repository.delete_organization(organization)
            await self.organization_repository.commit()
        except IntegrityError:
            await self.organization_repository.rollback()
            raise DataIntegrityError

