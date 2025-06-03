from typing import Sequence

from sqlalchemy import func, select

from src.core.models import Building
from src.core.repository.repository import SqlAlchemyRepository


class BuildingsRepository(SqlAlchemyRepository):
    model = Building

    async def get_buildings_by_radius(self, latitude: float, longitude: float, radius_km: float) -> Sequence[Building]:
        earth_radius_km = 6371

        haversine_distance = (
            earth_radius_km
            * 2
            * func.asin(
                func.sqrt(
                    func.pow(func.sin(func.radians((self.model.latitude - latitude) / 2)), 2)
                    + func.cos(func.radians(latitude))
                    * func.cos(func.radians(self.model.latitude))
                    * func.pow(func.sin(func.radians((self.model.longitude - longitude) / 2)), 2)
                )
            )
        )

        query = select(self.model).where(haversine_distance <= radius_km)
        result = await self.session.execute(query)
        buildings = result.scalars().all()
        return buildings
