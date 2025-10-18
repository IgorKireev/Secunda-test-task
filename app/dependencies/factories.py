from typing import Annotated, Type, TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure import get_session


T = TypeVar("T")


def repository_factory(repo_class: Type[T]):
    async def _get_repository(
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> T:
        return repo_class(session=session)

    return _get_repository
