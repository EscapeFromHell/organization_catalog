import logging

from fastapi import HTTPException
from pydantic import PositiveInt

from src.core.schemas import Activity, ActivityCreate, ActivityList, ActivityUpdate
from src.core.service.service import BaseService
from src.core.uow import transaction_mode
from src.utils import get_logger

logger = get_logger(__file__, log_level=logging.INFO)


class ActivitiesService(BaseService):
    base_repository: str = "activities"

    @transaction_mode
    async def __get_activity_level(self, activity_id: PositiveInt) -> PositiveInt:
        level = await self.uow.activities.get_activity_level(activity_id=activity_id)
        return level

    async def get_all_activities(self) -> ActivityList:
        result = await self.get_by_query_all()
        activities = [activity.to_pydantic_schema() for activity in result]
        activities_list = ActivityList(activities=activities)
        return activities_list

    async def get_activity_by_id(self, activity_id: PositiveInt) -> Activity:
        result = await self.get_by_query_one_or_none(id=activity_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Activity with ID: {activity_id} not found!")
        activity = result.to_pydantic_schema()
        return activity

    async def create_activity(self, activity: ActivityCreate) -> Activity:
        if activity.parent_id:
            parent_level = await self.__get_activity_level(activity_id=activity.parent_id)
            if parent_level >= 3:
                raise HTTPException(status_code=400, detail="Maximum activity depth is 3 levels")

        result = await self.add_one_and_get_obj(**activity.model_dump())
        created_activity = result.to_pydantic_schema()
        return created_activity

    async def update_activity(self, activity_id: PositiveInt, activity: ActivityUpdate) -> Activity:
        result = await self.update_one_by_id(obj_id=activity_id, **activity.model_dump())
        if not result:
            raise HTTPException(status_code=404, detail=f"Activity with ID: {activity_id} not found!")
        updated_activity = result.to_pydantic_schema()
        return updated_activity

    async def delete_activity(self, activity_id: PositiveInt) -> None:
        result = await self.get_by_query_one_or_none(id=activity_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Activity with ID: {activity_id} not found!")
        await self.delete_by_query(id=activity_id)
        logger.info(f"Activity with ID: {activity_id} deleted!")
