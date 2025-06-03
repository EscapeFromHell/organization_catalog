from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.orm import aliased, joinedload, selectinload

from src.core.models import Activity, Organization, OrganizationActivity
from src.core.repository.repository import SqlAlchemyRepository


class OrganizationsRepository(SqlAlchemyRepository):
    model = Organization

    async def add_activities_to_organization(self, organization_id: int, activity_ids: list[int]) -> None:
        query = insert(OrganizationActivity).values(
            [{"organization_id": organization_id, "activity_id": activity_id} for activity_id in activity_ids]
        )
        await self.session.execute(query)

    async def get_organization_with_activities_and_address(self, organization_id: int) -> Organization | None:
        query = (
            select(self.model)
            .options(joinedload(self.model.activities), joinedload(Organization.building))
            .where(self.model.id == organization_id)
        )
        result = await self.session.execute(query)
        result = result.unique()
        return result.scalar_one_or_none()

    async def get_organizations_by_activity_name(self, activity_name: str) -> Sequence[Organization]:
        query = (
            select(self.model)
            .join(self.model.activities)
            .filter(Activity.name == activity_name)
            .options(selectinload(Organization.activities))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_organizations_by_name(self, name: str) -> Sequence[Organization]:
        query = select(Organization).where(Organization.name.ilike(f"%{name}%"))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_organizations_by_activity_tree(self, activity_name: str) -> Sequence[Organization]:
        a = aliased(Activity)

        activity_tree = (
            select(Activity.id, Activity.parent_id, Activity.name)
            .where(Activity.name == activity_name)
            .cte(name="activity_tree", recursive=True)
        )

        activity_alias = aliased(activity_tree)

        activity_tree = activity_tree.union_all(
            select(a.id, a.parent_id, a.name).where(a.parent_id == activity_alias.c.id)
        )

        query = (
            select(Organization)
            .join(Organization.activities)
            .where(Organization.activities.any(Activity.id.in_(select(activity_tree.c.id))))
        )

        result = await self.session.execute(query)
        return result.scalars().all()
