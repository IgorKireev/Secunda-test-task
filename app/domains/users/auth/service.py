from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.domains.users.auth.repository import AuthRepository
from app.domains.users.models import User
from app.domains.users.schemas import UserRegister, UserLogin
from app.core.exceptions import (
    NotFoundError,
    Conflict,
    Unauthorized,
    DataIntegrityError,
)
from app.core.security import get_password_hash, verify_password, create_token


class AuthService:
    def __init__(self, auth_repository: AuthRepository) -> None:
        self.auth_repository = auth_repository

    async def register(self, user_data: UserRegister) -> dict:
        user = await self.auth_repository.get_user_by_email(user_data.email)
        if user:
            raise Conflict
        password = get_password_hash(user_data.password)
        user_orm = User(
            name=user_data.name,
            email=user_data.email,
            password=password,
        )
        try:
            user = await self.auth_repository.create_user(user_orm)
            username = user.name
            await self.auth_repository.commit()
            return {"message": f"Регистрация {username} прошла успешно!"}
        except IntegrityError as e:
            await self.auth_repository.rollback()
            raise DataIntegrityError(f"Could not create user: {str(e.orig)}")

    async def login(self, user_data: UserLogin) -> JSONResponse:
        user = await self.auth_repository.get_user_by_email(user_data.email)
        if not user:
            NotFoundError(entity="User")
        if not verify_password(user_data.password, user.password):
            raise Unauthorized
        access_token = create_token(
            {"sub": str(user.id), "role": user.role, "type": "access"},
            token_lifetime=600,
        )
        refresh_token = create_token(
            {"sub": str(user.id), "role": user.role, "type": "refresh"},
            token_lifetime=1200,
        )
        response = JSONResponse(
            content={"access_token": access_token, "token_type": "bearer"},
            status_code=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True
        )
        return response
