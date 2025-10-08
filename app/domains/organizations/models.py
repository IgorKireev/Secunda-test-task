from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure import association_table, Base
if TYPE_CHECKING:
    from app.domains.buildings.models import Building


class PhoneNumber(Base):
    __tablename__ = "numbers"

    phone_number: Mapped[str]
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="SET NULL"))
    organization: Mapped["Organization"] = relationship(back_populates="phone_numbers")