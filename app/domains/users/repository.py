from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_users(self) -> Sequence[User]:
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        return users

    async def get_user(self, user_id: int) -> User:
        query = select(User).filter(User.id == user_id)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
