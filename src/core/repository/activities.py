from sqlalchemy import select

from src.core.models import Activity
from src.core.repository.repository import SqlAlchemyRepository


class ActivitiesRepository(SqlAlchemyRepository):
    model = Activity

    async def get_ids_by_names(self, names: list[str]) -> list[int]:
        query = select(self.model.id).where(self.model.name.in_(names))
        result = await self.session.execute(query)
        return [row[0] for row in result.all()]

    async def get_activity_level(self, activity_id: int) -> int:
        level = 1
        current_id = activity_id

        while current_id:
            result = await self.session.execute(select(Activity.parent_id).where(Activity.id == current_id))
            parent_id = result.scalar_one_or_none()
            current_id = parent_id
            if current_id:
                level += 1

        return level
