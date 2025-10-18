from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure import association_table, Base

if TYPE_CHECKING:
    from app.domains.buildings.models import Building
    from app.domains.activities.models import Activity


class Organization(Base):
    __tablename__ = "organizations"

    title: Mapped[str] = mapped_column(String(30))
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="SET NULL")
    )
    phone_numbers: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    building: Mapped["Building"] = relationship(back_populates="organizations")
    activities: Mapped[list["Activity"]] = relationship(
        secondary=association_table, back_populates="organizations"
    )


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    phone_number: Mapped[str] = mapped_column(String(12))
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE")
    )
    organization: Mapped["Organization"] = relationship(back_populates="phone_numbers")
