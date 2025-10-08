from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure import association_table, Base


class Activity(Base):
    __tablename__ = "activities"

    name: Mapped[str] = mapped_column(String(30))
    organizations: Mapped[list["association_table"]] = relationship(back_populates="activities")
