from sqlalchemy import Column, Table, ForeignKey
from app.infrastructure.db import Base


association_table = Table(
    "association_table",
    Base.metadata,
    Column("organization_id", ForeignKey("organization.id")),
    Column("activity_id", ForeignKey("activities.id")),
)