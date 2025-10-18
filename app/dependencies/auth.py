from typing import Annotated

from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.security import create_token, get_token_payload
from app.dependencies.services import get_user_service
from app.domains.users.models import User
from app.core.exceptions import Forbidden, Unauthorized
from app.domains.users.service import UserService
from app.settings import get_settings


settings = get_settings()
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_refresh_token_payload_by_cookie(
    refresh_token: str | None = Cookie(None),
) -> dict:
    return get_token_payload(token=refresh_token, token_type="refresh")


def get_access_token(access_token: Annotated[str, Depends(OAuth2_scheme)]) -> dict:
    return get_token_payload(token=access_token, token_type="access")


def update_access_token(refresh_token_payload: dict):
    token_type = refresh_token_payload.get("type")
    if not token_type == "refresh":
        raise Forbidden("Invalid token type, refresh token expected")
    new_access_token = create_token(
        {
            "sub": refresh_token_payload.get("sub"),
            "role": refresh_token_payload.get("role"),
            "type": "access",
        },
        token_lifetime=600,
    )
    return {"access_token": new_access_token}


async def get_current_user(
    payload: Annotated[dict, Depends(get_access_token)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise Unauthorized(message="Invalid token payload: 'sub' must be an integer")
    user = await user_service.get_user(user_id=user_id)
    return user


def role_required(required_roles: list[str]):
    def wrapper(user: Annotated[User, Depends(get_current_user)]) -> None:
        if user.role not in required_roles:
            raise Forbidden(message="Insufficient rights")

    return wrapper
