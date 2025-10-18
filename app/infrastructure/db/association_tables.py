from sqlalchemy import Column, Table, ForeignKey
from app.infrastructure.db.base_model import Base


association_table = Table(
    "association_table",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)
