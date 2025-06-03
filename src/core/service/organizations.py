import logging
from typing import List

from fastapi import HTTPException
from pydantic import PositiveInt

from src.core.schemas import OrganizationCreate, OrganizationDetailed, OrganizationList, OrganizationUpdate
from src.core.service.service import BaseService
from src.core.uow import transaction_mode
from src.utils import get_logger

logger = get_logger(__file__, log_level=logging.INFO)


class OrganizationsService(BaseService):
    base_repository: str = "organizations"

    @transaction_mode
    async def __get_ids_by_names(self, activities: List[str]) -> list[PositiveInt]:
        activity_ids = await self.uow.activities.get_ids_by_names(names=activities)
        return activity_ids

    @transaction_mode
    async def __check_building(self, building_id: PositiveInt) -> bool:
        building = await self.uow.buildings.get_by_query_one_or_none(id=building_id)
        return True if building else False

    @transaction_mode
    async def __get_organizations_by_name(self, organization_name: str) -> OrganizationList:
        result = await self.uow.organizations.get_organizations_by_name(name=organization_name)
        organizations = [organization.to_pydantic_schema() for organization in result]
        return OrganizationList(organizations=organizations)

    @transaction_mode
    async def __get_organizations_by_activity_name(self, activity_name: str) -> OrganizationList:
        result = await self.uow.organizations.get_organizations_by_activity_name(activity_name=activity_name)
        organizations = [organization.to_pydantic_schema() for organization in result]
        return OrganizationList(organizations=organizations)

    @transaction_mode
    async def __get_organizations_by_activity_tree(self, activity_name: str) -> OrganizationList:
        result = await self.uow.organizations.get_organizations_by_activity_tree(activity_name=activity_name)
        organizations = [organization.to_pydantic_schema() for organization in result]
        return OrganizationList(organizations=organizations)

    @transaction_mode
    async def __add_activities_to_organization(
        self, organization_id: PositiveInt, activity_ids: list[PositiveInt]
    ) -> None:
        return await self.uow.organizations.add_activities_to_organization(
            organization_id=organization_id, activity_ids=activity_ids
        )

    @transaction_mode
    async def __get_organizations_by_radius(
        self, latitude: float, longitude: float, radius_km: float
    ) -> OrganizationList:
        result = await self.uow.buildings.get_buildings_by_radius(
            latitude=latitude, longitude=longitude, radius_km=radius_km
        )
        building_ids = [building.id for building in result]
        organizations_by_radius = []
        for building_id in building_ids:
            organizations = await self.get_by_query_all(building_id=building_id)
            organizations = [organization.to_pydantic_schema() for organization in organizations]
            organizations_by_radius += organizations
        return OrganizationList(organizations=organizations_by_radius)

    @transaction_mode
    async def __get_organization_with_activities_and_address(
        self, organization_id: PositiveInt
    ) -> OrganizationDetailed | None:
        organization = await self.uow.organizations.get_organization_with_activities_and_address(
            organization_id=organization_id
        )
        if not organization:
            return None
        activities = [activity.name for activity in organization.activities]
        address = organization.building.address
        organization = organization.to_pydantic_schema_detailed(address=address, activities=activities)
        return organization

    async def get_all_organizations(self) -> OrganizationList:
        result = await self.get_by_query_all()
        organizations = [organization.to_pydantic_schema() for organization in result]
        organizations_list = OrganizationList(organizations=organizations)
        return organizations_list

    async def get_organization_by_id(self, organization_id: PositiveInt) -> OrganizationDetailed:
        organization = await self.__get_organization_with_activities_and_address(organization_id=organization_id)
        if not organization:
            raise HTTPException(status_code=404, detail=f"Organization with ID: {organization_id} not found!")
        return organization

    async def create_organization(
        self, organization: OrganizationCreate, activities: List[str]
    ) -> OrganizationDetailed:
        if not await self.__check_building(building_id=organization.building_id):
            raise HTTPException(status_code=404, detail=f"Building with ID: {organization.building_id} not found!")
        activity_ids = await self.__get_ids_by_names(activities=activities)
        organization_obj = await self.add_one_and_get_obj(**organization.model_dump())
        await self.__add_activities_to_organization(organization_id=organization_obj.id, activity_ids=activity_ids)
        created_organization = await self.__get_organization_with_activities_and_address(
            organization_id=organization_obj.id
        )
        return created_organization

    async def update_organization(
        self, organization_id: PositiveInt, organization: OrganizationUpdate
    ) -> OrganizationDetailed:
        result = await self.update_one_by_id(obj_id=organization_id, **organization.model_dump())
        if not result:
            raise HTTPException(status_code=404, detail=f"Organization with ID: {organization_id} not found!")
        updated_organization = await self.__get_organization_with_activities_and_address(
            organization_id=organization_id
        )
        return updated_organization

    async def delete_organization(self, organization_id: PositiveInt) -> None:
        result = await self.get_by_query_one_or_none(id=organization_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Organization with ID: {organization_id} not found!")
        await self.delete_by_query(id=organization_id)
        logger.info(f"Order with order_id {organization_id} deleted!")

    async def get_organizations_by_building_id(self, building_id: PositiveInt) -> OrganizationList:
        result = await self.get_by_query_all(building_id=building_id)
        organizations = [organization.to_pydantic_schema() for organization in result]
        return OrganizationList(organizations=organizations)

    async def get_organizations_by_activity_name(self, activity_name: str) -> OrganizationList:
        return await self.__get_organizations_by_activity_name(activity_name=activity_name)

    async def get_organizations_by_name(self, organization_name: str) -> OrganizationList:
        return await self.__get_organizations_by_name(organization_name=organization_name)

    async def get_organizations_by_activity_tree(self, activity_name: str) -> OrganizationList:
        return await self.__get_organizations_by_activity_tree(activity_name=activity_name)

    async def get_organizations_by_radius(self, latitude: float, longitude: float, radius_km: float):
        return await self.__get_organizations_by_radius(latitude=latitude, longitude=longitude, radius_km=radius_km)
