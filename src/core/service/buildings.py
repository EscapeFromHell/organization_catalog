import logging

from fastapi import HTTPException
from pydantic import PositiveInt

from src.core.schemas import Building, BuildingCreate, BuildingList, BuildingUpdate
from src.core.service.service import BaseService
from src.core.uow import transaction_mode
from src.utils import get_logger

logger = get_logger(__file__, log_level=logging.INFO)


class BuildingsService(BaseService):
    base_repository: str = "buildings"

    @transaction_mode
    async def __get_buildings_by_radius(self, latitude: float, longitude: float, radius_km: float) -> BuildingList:
        result = await self.uow.buildings.get_buildings_by_radius(
            latitude=latitude, longitude=longitude, radius_km=radius_km
        )
        buildings = [building.to_pydantic_schema() for building in result]
        return BuildingList(buildings=buildings)

    async def get_all_buildings(self) -> BuildingList:
        result = await self.get_by_query_all()
        buildings = [building.to_pydantic_schema() for building in result]
        buildings_list = BuildingList(buildings=buildings)
        return buildings_list

    async def get_building_by_id(self, building_id: PositiveInt) -> Building:
        result = await self.get_by_query_one_or_none(id=building_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Building with ID: {building_id} not found!")
        building = result.to_pydantic_schema()
        return building

    async def get_buildings_by_radius(self, latitude: float, longitude: float, radius_km: float) -> BuildingList:
        return await self.__get_buildings_by_radius(latitude=latitude, longitude=longitude, radius_km=radius_km)

    async def create_building(self, building: BuildingCreate) -> Building:
        result = await self.add_one_and_get_obj(**building.model_dump())
        created_building = result.to_pydantic_schema()
        return created_building

    async def update_building(self, building_id: PositiveInt, building: BuildingUpdate) -> Building:
        result = await self.update_one_by_id(obj_id=building_id, **building.model_dump())
        if not result:
            raise HTTPException(status_code=404, detail=f"Building with ID: {building_id} not found!")
        updated_building = result.to_pydantic_schema()
        return updated_building

    async def delete_building(self, building_id: PositiveInt) -> None:
        result = await self.get_by_query_one_or_none(id=building_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Building with ID: {building_id} not found!")
        await self.delete_by_query(id=building_id)
        logger.info(f"Building with ID: {building_id} deleted!")
