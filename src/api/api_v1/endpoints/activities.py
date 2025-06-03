from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.core.schemas import Activity, ActivityCreate, ActivityList, ActivityUpdate
from src.core.service.activities import ActivitiesService

router = APIRouter()


@router.get("", status_code=200, response_model=ActivityList)
async def get_all_activities(activities_service: ActivitiesService = Depends(ActivitiesService)) -> ActivityList:
    """
    Retrieve a list of all activities.

    :param activities_service: Service for handling activity-related operations.
    """
    return await activities_service.get_all_activities()


@router.get("/{activity_id}", status_code=200, response_model=Activity)
async def get_activity_by_id(
    activity_id: PositiveInt, activities_service: ActivitiesService = Depends(ActivitiesService)
) -> Activity:
    """
    Retrieve a specific activity by its ID.

    :param activity_id: ID of the activity to retrieve.
    :param activities_service: Service for handling activity-related operations.
    """
    return await activities_service.get_activity_by_id(activity_id=activity_id)


@router.post("", status_code=201, response_model=Activity)
async def create_activity(
    activity: ActivityCreate,
    activities_service: ActivitiesService = Depends(ActivitiesService),
) -> Activity:
    """
    Create a new activity.

    :param activity: Data for the activity to be created.
    :param activities_service: Service for handling activity-related operations.
    """
    return await activities_service.create_activity(activity=activity)


@router.put("/{activity_id}", status_code=200, response_model=Activity)
async def update_activity(
    activity_id: PositiveInt,
    activity: ActivityUpdate,
    activities_service: ActivitiesService = Depends(ActivitiesService),
) -> Activity:
    """
    Update an existing activity by its ID.

    :param activity_id: ID of the activity to update.
    :param activity: Updated data for the activity.
    :param activities_service: Service for handling activity-related operations.
    """
    return await activities_service.update_activity(activity_id=activity_id, activity=activity)


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: PositiveInt, activities_service: ActivitiesService = Depends(ActivitiesService)
) -> None:
    """
    Delete an activity by its ID.

    :param activity_id: ID of the activity to delete.
    :param activities_service: Service for handling activity-related operations.
    """
    return await activities_service.delete_activity(activity_id=activity_id)
