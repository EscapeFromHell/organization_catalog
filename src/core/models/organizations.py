from typing import Optional

import sqlalchemy.orm as so
from sqlalchemy import ForeignKey

from src.core.models.base import BaseModel
from src.core.schemas import Organization as OrganizationSchema
from src.core.schemas import OrganizationDetailed


class OrganizationActivity(BaseModel):
    __tablename__ = "organization_activity"

    organization_id: so.Mapped[int] = so.mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True
    )
    activity_id: so.Mapped[int] = so.mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)


class Organization(BaseModel):
    __tablename__ = "organizations"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    name: so.Mapped[str] = so.mapped_column(nullable=False)
    phones: so.Mapped[str] = so.mapped_column(nullable=False)
    building_id: so.Mapped[int] = so.mapped_column(ForeignKey("buildings.id"), nullable=True)
    building: so.Mapped["Building"] = so.relationship()
    activities: so.Mapped[list["Activity"]] = so.relationship(
        secondary="organization_activity", backref="organizations"
    )

    def to_pydantic_schema(self) -> OrganizationSchema:
        return OrganizationSchema(id=self.id, name=self.name, phones=self.phones, building_id=self.building_id)

    def to_pydantic_schema_detailed(self, address: str, activities: Optional[list[str]] = None) -> OrganizationDetailed:
        return OrganizationDetailed(
            id=self.id,
            name=self.name,
            phones=self.phones,
            building_id=self.building_id,
            address=address,
            activities=activities,
        )
