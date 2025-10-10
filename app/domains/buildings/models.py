from typing import TYPE_CHECKING
from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure import Base
if TYPE_CHECKING:
    from app.domains.organizations.models import Organization


class Building(Base):
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(String(50))
    latitude: Mapped[float] = mapped_column(DECIMAL(9, 6), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6), nullable=False)
    organizations: Mapped[list["Organization"]] = relationship(back_populates="building")