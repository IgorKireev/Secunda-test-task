from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure import Base
from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )
    password: Mapped[str] = mapped_column(String(128))
    role: Mapped[Role] = mapped_column(
        Enum(Role, values_callable=lambda x: [e.value for e in x]),
        default=Role.USER
    )