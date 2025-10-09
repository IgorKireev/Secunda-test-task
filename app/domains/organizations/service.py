from xml.dom.minidom import Entity

from app.domains.organizations.models import Organization
from app.domains.organizations.repository import OrganizationRepository
from app.domains.organizations.schemas import OrganizationRead, OrganizationRelDTO
from app.exceptions.exceptions import NotFoundError


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository) -> None:
        self.organization_repository = organization_repository

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




