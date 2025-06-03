import sqlalchemy.orm as so

from src.core.models.base import BaseModel
from src.core.schemas import Building as BuildingSchema


class Building(BaseModel):
    __tablename__ = "buildings"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    address: so.Mapped[str] = so.mapped_column(nullable=False)
    latitude: so.Mapped[float] = so.mapped_column(nullable=False)
    longitude: so.Mapped[float] = so.mapped_column(nullable=False)

    def to_pydantic_schema(self) -> BuildingSchema:
        return BuildingSchema(
            id=self.id,
            address=self.address,
            latitude=self.latitude,
            longitude=self.longitude,
        )
