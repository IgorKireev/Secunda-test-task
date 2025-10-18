from sqlalchemy.exc import IntegrityError
from app.domains.users.models import User
from app.domains.users.repository import UserRepository
from app.domains.users.schemas import UserDTO, UserCreate
from app.core.security import get_password_hash
from app.core.exceptions import NotFoundError, DataIntegrityError


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_users(self) -> list[UserDTO]:
        users_orm = await self.user_repository.get_users()
        users = [UserDTO.model_validate(user) for user in users_orm]
        return users

    async def get_user(self, user_id: int) -> UserDTO | None:
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise NotFoundError(entity="User")
        return UserDTO.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserDTO:
        password = get_password_hash(user_data.password)
        user_orm = User(
            name=user_data.name,
            email=user_data.email,
            password=password,
            role=user_data.role,
        )
        try:
            user = await self.user_repository.create_user(user_orm)
            user_id = user.id
            await self.user_repository.commit()
            reloaded_user = await self.user_repository.get_user(user_id)
            return UserDTO.model_validate(reloaded_user)
        except IntegrityError as e:
            await self.user_repository.rollback()
            raise DataIntegrityError(f"Could not create user: {str(e.orig)}")

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise NotFoundError(entity="User")
        try:
            await self.user_repository.delete_user(user)
            await self.user_repository.commit()
        except IntegrityError:
            await self.user_repository.rollback()
            raise DataIntegrityError
