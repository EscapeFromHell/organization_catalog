from typing import List

from pydantic import BaseModel, PositiveInt


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingInDB(BuildingBase):
    id: PositiveInt

    class Config:
        from_attributes = True


class Building(BuildingInDB):
    pass


class BuildingList(BaseModel):
    buildings: List[Building]
