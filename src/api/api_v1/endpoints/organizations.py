from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import PositiveInt

from src.core.schemas import OrganizationCreate, OrganizationDetailed, OrganizationList, OrganizationUpdate
from src.core.service.organizations import OrganizationsService

router = APIRouter()


@router.get("", status_code=200, response_model=OrganizationList)
async def get_all_organizations(
    organizations_service: OrganizationsService = Depends(OrganizationsService),
) -> OrganizationList:
    """
    Retrieve a list of all organizations.

    :param organizations_service: Service for handling organization-related operations.
    """
    return await organizations_service.get_all_organizations()


@router.get("/by_name", status_code=200, response_model=OrganizationList)
async def get_organizations_by_name(
    organization_name: str, organization_service: OrganizationsService = Depends(OrganizationsService)
) -> OrganizationList:
    """
    Retrieve organizations by their name.

    :param organization_name: Name or partial name of the organization.
    :param organization_service: Service for handling organization-related operations.
    """
    return await organization_service.get_organizations_by_name(organization_name=organization_name)


@router.get("/by_activity", status_code=200, response_model=OrganizationList)
async def get_organizations_by_activity_name(
    activity_name: str, organization_service: OrganizationsService = Depends(OrganizationsService)
) -> OrganizationList:
    """
    Retrieve organizations that are associated with a specific activity name.

    :param activity_name: Name of the activity.
    :param organization_service: Service for handling organization-related operations.
    """
    return await organization_service.get_organizations_by_activity_name(activity_name=activity_name)


@router.get("/by_activity_tree", status_code=200, response_model=OrganizationList)
async def get_organizations_by_activity_tree(
    activity_name: str, organization_service: OrganizationsService = Depends(OrganizationsService)
) -> OrganizationList:
    """
    Retrieve organizations by activity name, including nested sub-activities (up to 3 levels deep).

    :param activity_name: Name of the parent activity.
    :param organization_service: Service for handling organization-related operations.
    """
    return await organization_service.get_organizations_by_activity_tree(activity_name=activity_name)


@router.get("/by_radius", response_model=OrganizationList)
async def get_organizations_by_radius(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(...),
    organizations_service: OrganizationsService = Depends(OrganizationsService),
) -> OrganizationList:
    """
    Retrieve organizations located within a specified radius from given coordinates.

    :param latitude: Latitude of the center point.
    :param longitude: Longitude of the center point.
    :param radius_km: Radius in kilometers.
    :param organizations_service: Service for handling organization-related operations.
    """
    return await organizations_service.get_organizations_by_radius(
        latitude=latitude, longitude=longitude, radius_km=radius_km
    )


@router.get("/{organization_id}", status_code=200, response_model=OrganizationDetailed)
async def get_organization_by_id(
    organization_id: PositiveInt,
    organizations_service: OrganizationsService = Depends(OrganizationsService),
) -> OrganizationDetailed:
    """
    Retrieve detailed information about an organization by its ID.

    :param organization_id: ID of the organization.
    :param organizations_service: Service for handling organization-related operations.
    """
    return await organizations_service.get_organization_by_id(organization_id=organization_id)


@router.get("/by_building/{building_id}", status_code=200, response_model=OrganizationList)
async def get_organizations_by_building_id(
    building_id: PositiveInt, organization_service: OrganizationsService = Depends(OrganizationsService)
) -> OrganizationList:
    """
    Retrieve organizations located in a specific building.

    :param building_id: ID of the building.
    :param organization_service: Service for handling organization-related operations.
    """
    return await organization_service.get_organizations_by_building_id(building_id=building_id)


@router.post("", status_code=201, response_model=OrganizationDetailed)
async def create_organization(
    organization: OrganizationCreate,
    activities: List[str],
    organizations_service: OrganizationsService = Depends(OrganizationsService),
) -> OrganizationDetailed:
    """
    Create a new organization and associate it with a list of activity names.

    :param organization: Organization creation data.
    :param activities: List of activity names to associate with the organization.
    :param organizations_service: Service for handling organization-related operations.
    """
    return await organizations_service.create_organization(organization=organization, activities=activities)


@router.put("/{organization_id}", status_code=201, response_model=OrganizationDetailed)  # TODO change activity
async def update_order(
    organization_id: PositiveInt,
    organization: OrganizationUpdate,
    organization_service: OrganizationsService = Depends(OrganizationsService),
) -> OrganizationDetailed:
    """
    Update organization information by ID.

    :param organization_id: ID of the organization to update.
    :param organization: Updated organization data.
    :param organization_service: Service for handling organization-related operations.
    """
    return await organization_service.update_organization(organization_id=organization_id, organization=organization)


@router.delete("/{organization_id}", status_code=204)
async def delete_organization(
    organization_id: PositiveInt, organization_service: OrganizationsService = Depends(OrganizationsService)
) -> None:
    """
    Delete an organization by its ID.

    :param organization_id: ID of the organization to delete.
    :param organization_service: Service for handling organization-related operations.
    """
    return await organization_service.delete_organization(organization_id=organization_id)
