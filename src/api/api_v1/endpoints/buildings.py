from fastapi import APIRouter, Depends, Query
from pydantic import PositiveInt

from src.core.schemas import Building, BuildingCreate, BuildingList, BuildingUpdate
from src.core.service.buildings import BuildingsService

router = APIRouter()


@router.get("", status_code=200, response_model=BuildingList)
async def get_all_buildings(buildings_service: BuildingsService = Depends(BuildingsService)) -> BuildingList:
    """
    Retrieve a list of all buildings.

    :param buildings_service: Service for handling building-related operations.
    """
    return await buildings_service.get_all_buildings()


@router.get("/{building_id}", status_code=200, response_model=Building)
async def get_building_by_id(
    building_id: PositiveInt, building_service: BuildingsService = Depends(BuildingsService)
) -> Building:
    """
    Retrieve a specific building by its ID.

    :param building_id: ID of the building to retrieve.
    :param building_service: Service for handling building-related operations.
    """
    return await building_service.get_building_by_id(building_id=building_id)


@router.get("/buildings_by_radius", response_model=BuildingList)
async def get_buildings_by_radius(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(...),
    building_service: BuildingsService = Depends(BuildingsService),
) -> BuildingList:
    """
    Retrieve buildings located within a specified radius from given coordinates.

    :param latitude: Latitude of the center point.
    :param longitude: Longitude of the center point.
    :param radius_km: Radius in kilometers.
    :param building_service: Service for handling building-related operations.
    """
    return await building_service.get_buildings_by_radius(latitude=latitude, longitude=longitude, radius_km=radius_km)


@router.post("", status_code=201, response_model=Building)
async def create_building(
    building: BuildingCreate,
    buildings_service: BuildingsService = Depends(BuildingsService),
) -> Building:
    """
    Create a new building.

    :param building: Data for the building to be created.
    :param buildings_service: Service for handling building-related operations.
    """
    return await buildings_service.create_building(building=building)


@router.put("/{building_id}", status_code=200, response_model=Building)
async def update_building(
    building_id: PositiveInt, building: BuildingUpdate, building_service: BuildingsService = Depends(BuildingsService)
) -> Building:
    """
    Update an existing building by its ID.

    :param building_id: ID of the building to update.
    :param building: Updated data for the building.
    :param building_service: Service for handling building-related operations.
    """
    return await building_service.update_building(building_id=building_id, building=building)


@router.delete("/{building_id}", status_code=204)
async def delete_building(
    building_id: PositiveInt, building_service: BuildingsService = Depends(BuildingsService)
) -> None:
    """
    Delete a building by its ID.

    :param building_id: ID of the building to delete.
    :param building_service: Service for handling building-related operations.
    """
    return await building_service.delete_building(building_id=building_id)
