from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_auth_service
from app.dependencies.auth import (
    get_refresh_token_payload_by_cookie,
    update_access_token,
)
from app.domains.users.schemas import UserRegister, UserLogin
from app.domains.users.auth.service import AuthService


router = APIRouter(tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user_data: UserRegister,
):
    return await auth_service.register(user_data)


@router.post("/login")
async def login_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user_data: UserLogin,
):
    return await auth_service.login(user_data)


@router.post("/refresh")
async def update_access_token(
    refresh_token_payload: Annotated[
        dict, Depends(get_refresh_token_payload_by_cookie)
    ],
):
    return update_access_token(refresh_token_payload)
