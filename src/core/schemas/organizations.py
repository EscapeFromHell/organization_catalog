from typing import List

from pydantic import BaseModel, PositiveInt


class OrganizationBase(BaseModel):
    name: str
    phones: str
    building_id: PositiveInt


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationInDB(OrganizationBase):
    id: PositiveInt

    class Config:
        from_attributes = True


class Organization(OrganizationInDB):
    pass


class OrganizationDetailed(OrganizationInDB):
    address: str
    activities: List[str]


class OrganizationList(BaseModel):
    organizations: List[Organization]
