from fastapi import APIRouter, Depends

from src.api.api_v1.endpoints import activities_router, buildings_router, organizations_router
from src.config.security import get_api_key

api_router = APIRouter(dependencies=[Depends(get_api_key)])

api_router.include_router(activities_router, prefix="/activities", tags=["activities"])
api_router.include_router(buildings_router, prefix="/buildings", tags=["buildings"])
api_router.include_router(organizations_router, prefix="/organizations", tags=["organizations"])
