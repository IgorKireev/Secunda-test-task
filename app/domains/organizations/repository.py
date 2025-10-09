from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.domains import Organization


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_organizations(self) -> Sequence[Organization]:
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

    async def create_organization(self, organization: Organization) -> Organization:
        self.session.add(organization)
        await self.session.flush()
        return organization

    async def delete_organization(self, organization: Organization) -> None:
        await self.session.delete(organization)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()