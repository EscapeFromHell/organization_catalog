import sqlalchemy.orm as so
from sqlalchemy import ForeignKey

from src.core.models.base import BaseModel
from src.core.schemas import Activity as ActivitySchema


class Activity(BaseModel):
    __tablename__ = "activities"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    name: so.Mapped[str] = so.mapped_column(nullable=False)
    parent_id: so.Mapped[int] = so.mapped_column(ForeignKey("activities.id"), nullable=True)
    parent: so.Mapped["Activity"] = so.relationship(remote_side=[id], backref="subactivities")

    def to_pydantic_schema(self) -> ActivitySchema:
        return ActivitySchema(
            id=self.id,
            name=self.name,
            parent_id=self.parent_id,
        )
