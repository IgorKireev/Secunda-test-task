from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.domains import Organization, OrganizationCreate
from app.domains.organizations.schemas import PhoneNumber


class OrganizationRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_organizations(self) -> list[Organization]:
        query = (
            select(Organization)
            .options(joinedload(Organization.building))
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
        )
        organizations = await self.session.execute(query)
        return organizations.unique().scalars().all()

    async def get_organization(self, organization_id: int) -> Organization | None:
        query = (
            select(Organization)
            .filter(Organization.id == organization_id)
            .options(joinedload(Organization.building))
            .options(selectinload(Organization.phone_numbers))
            .options(selectinload(Organization.activities))
        )
        organization = await self.session.execute(query)
        return organization.scalar_one_or_none()
