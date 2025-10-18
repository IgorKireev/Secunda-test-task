from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.dependencies import get_user_service
from app.domains.users.schemas import UserCreate, UserResponse
from app.domains.users.service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить всех пользователей",
    description="Возвращает список всех пользователей",
)
async def get_users(
        user_service: Annotated[
            UserService,
            Depends(get_user_service)
        ]
    ):
    return await user_service.get_users()

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя по ID",
    description="Возвращает информацию о конкретном пользователе",
)
async def get_user(
        user_service: Annotated[
            UserService,
            Depends(get_user_service)
        ],
        user_id: int
    ):
    return await user_service.get_user(user_id)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    description="Создает нового пользователя",
)
async def create_user(
        user_service: Annotated[
            UserService,
            Depends(get_user_service)
        ],
        user_data: UserCreate
    ):
    return await user_service.create_user(user_data)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя",
    description="Удаляет пользователя из системы",
)
async def delete_user(
        user_service: Annotated[
            UserService,
            Depends(get_user_service)
        ],
        user_id: int
    ):
    return await user_service.delete_user(user_id)