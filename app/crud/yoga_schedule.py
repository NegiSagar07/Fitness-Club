"""
This module contains CRUD operations for the YogaSchedule model.
It provides functions to create, read, update, and delete yoga schedules in the database.
Each function interacts with the database session to perform the necessary operations on the YogaSchedule model,
ensuring that the data is correctly managed and persisted. The functions are designed to be used in
the route handlers for managing yoga schedules in the application.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Schedule 


async def create_yoga_schedule(db: AsyncSession, schedule: Schedule) -> Schedule:
    schedule = Schedule(
        yoga_class_id=schedule.yoga_class_id,
        instructor_id=schedule.instructor_id,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        weekday=schedule.weekday
    )

    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


async def get_yoga_schedule_by_id(db: AsyncSession, schedule_id: int) -> Schedule:
    result = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    schedule = result.scalars().first()
    return schedule


async def update_yoga_schedule(db: AsyncSession, schedule_id: int, updated_schedule: Schedule) -> Schedule:
    existing_schedule = await get_yoga_schedule_by_id(db, schedule_id)
    if not existing_schedule:
        return None
    
    existing_schedule.yoga_class_id = updated_schedule.yoga_class_id    
    existing_schedule.instructor_id = updated_schedule.instructor_id
    existing_schedule.start_time = updated_schedule.start_time
    existing_schedule.end_time = updated_schedule.end_time
    existing_schedule.weekday = updated_schedule.weekday

    await db.commit()
    await db.refresh(existing_schedule)
    return existing_schedule


async def delete_yoga_schedule(db: AsyncSession, schedule_id: int) -> bool:
    existing_schedule = await get_yoga_schedule_by_id(db, schedule_id)
    if not existing_schedule:
        return False
    
    await db.delete(existing_schedule)
    await db.commit()
    return True



