from typing import List

from pydantic import BaseModel, PositiveInt


class ActivityBase(BaseModel):
    name: str
    parent_id: PositiveInt | None = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    pass


class ActivityInDB(ActivityBase):
    id: PositiveInt

    class Config:
        from_attributes = True


class Activity(ActivityInDB):
    pass


class ActivityList(BaseModel):
    activities: List[Activity]
