"""
This module contains CRUD operations for the YogaSession model.
It provides functions to create, read, update, and delete yoga sessions in the database. 
Each function interacts with the database session to perform the necessary operations on the YogaSession model, 
ensuring that the data is correctly managed and persisted. The functions are designed to be used in the route handlers 
for managing yoga sessions in the application.
"""


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import YogaSession
from app.schema import YogaSessionCreate, YogaSessionUpdate


async def create_yoga_session(db: AsyncSession, yoga_session: YogaSessionCreate) -> YogaSession:
    yoga_session = YogaSession(
        yoga_class_id=yoga_session.yoga_class_id,
        instructor_id=yoga_session.instructor_id,
        start_time=yoga_session.start_time,
        end_time=yoga_session.end_time,
        max_capacity=yoga_session.max_capacity,
    )

    db.add(yoga_session)
    await db.commit()
    await db.refresh(yoga_session)
    return yoga_session


async def get_yoga_session_by_id(db: AsyncSession, yoga_session_id: int) -> YogaSession:
    result = await db.execute(select(YogaSession).where(YogaSession.id == yoga_session_id))
    yoga_session = result.scalars().first()
    return yoga_session


async def update_yoga_session(db: AsyncSession, yoga_session_id: int, updated_session: YogaSessionUpdate) -> YogaSession:
    existing_session = await get_yoga_session_by_id(db, yoga_session_id)
    if not existing_session:
        return None

    update_data = updated_session.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_session, field, value)

    await db.commit()
    await db.refresh(existing_session)
    return existing_session


async def delete_yoga_session(db: AsyncSession, yoga_session_id: int) -> bool:
    existing_session = await get_yoga_session_by_id(db, yoga_session_id)
    if not existing_session:
        return False
    
    await db.delete(existing_session)
    await db.commit()
    return True

