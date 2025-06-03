import random

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Activity, Building, Organization, OrganizationActivity


async def seed_data(session: AsyncSession) -> None:
    result = await session.execute(select(Building))
    if result.scalars().first():
        return None

    buildings = [
        Building(address=f"{i} Example St", latitude=55.75 + i * 0.001, longitude=37.61 + i * 0.001)
        for i in range(1, 11)
    ]
    session.add_all(buildings)
    await session.flush()

    activities = {
        "Retail": Activity(name="Retail"),
        "Logistics": Activity(name="Logistics"),
        "IT": Activity(name="IT"),
        "Consulting": Activity(name="Consulting"),
        "Education": Activity(name="Education"),
    }
    session.add_all(activities.values())
    await session.flush()

    nested_activities = {
        "IT Support": Activity(name="IT Support", parent_id=activities["IT"].id),
        "IT Infrastructure": Activity(name="IT Infrastructure", parent_id=activities["IT"].id),
        "Consulting B2B": Activity(name="Consulting B2B", parent_id=activities["Consulting"].id),
        "Consulting B2C": Activity(name="Consulting B2C", parent_id=activities["Consulting"].id),
    }
    session.add_all(nested_activities.values())
    await session.flush()

    deep_nested = Activity(name="Consulting B2C Small", parent_id=nested_activities["Consulting B2C"].id)
    session.add(deep_nested)
    await session.flush()

    all_activities = list(activities.values()) + list(nested_activities.values()) + [deep_nested]
    activity_map = {a.name: a for a in all_activities}

    organizations = [
        Organization(name=f"Organization {i}", phones=f"+7-900-000-00{i:02}", building_id=random.choice(buildings).id)
        for i in range(1, 21)
    ]
    session.add_all(organizations)
    await session.flush()

    activity_profiles = [
        ["Retail"],
        ["Logistics"],
        ["IT", "IT Support"],
        ["IT", "IT Infrastructure"],
        ["Education"],
        ["Consulting", "Consulting B2B"],
        ["Consulting", "Consulting B2C"],
        ["Consulting", "Consulting B2C", "Consulting B2C Small"],
        ["Retail", "Logistics"],
        ["IT", "Consulting"],
    ]

    organization_activity_links = []
    for i, org in enumerate(organizations):
        profile = activity_profiles[i % len(activity_profiles)]
        for act_name in profile:
            activity_id = activity_map[act_name].id
            organization_activity_links.append({"organization_id": org.id, "activity_id": activity_id})

    await session.execute(insert(OrganizationActivity), organization_activity_links)
    await session.commit()
