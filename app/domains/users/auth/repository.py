from sqlalchemy import select

from app.domains.users.models import User
from app.domains.users.repository import UserRepository


class AuthRepository(UserRepository):
    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).filter(User.email == email)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
