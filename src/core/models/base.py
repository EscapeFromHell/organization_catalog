import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(AsyncAttrs, so.DeclarativeBase):
    pass
