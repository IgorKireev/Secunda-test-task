from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure import association_table, Base

if TYPE_CHECKING:
    from app.domains.organizations.models import Organization


class Activity(Base):
    __tablename__ = "activities"

    name: Mapped[str] = mapped_column(String(30))
    organizations: Mapped[list["Organization"]] = relationship(
        secondary=association_table, back_populates="activities"
    )
