"""
This module contains CRUD operations for the Instructor model.
We will implement the following functions:
- create_instructor(db: AsyncSession, name, bio) -> InstructorResponse
- get_instructor_by_id(db: AsyncSession, instructor_id) -> Optional[InstructorResponse]
- update_instructor(db: AsyncSession, instructor_id, name, bio) -> Optional[InstructorResponse]
- delete_instructor(db: AsyncSession, instructor_id) -> bool
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models import Instructor
from app.schema import InstructorCreate, InstructorResponse
from typing import Optional 


async def create_instructor(db: AsyncSession, instructor: InstructorCreate) -> InstructorResponse:
    new_instructor = Instructor(
        name=instructor.name,
        bio=instructor.bio
    )
    db.add(new_instructor)
    await db.commit()
    await db.refresh(new_instructor)
    return new_instructor


async def get_instructor_by_id(db: AsyncSession, instructor_id: int) -> Optional[InstructorResponse]:
    result = await db.execute(select(Instructor).where(Instructor.id == instructor_id))
    instructor = result.scalars().first()
    return instructor


async def update_instructor(db: AsyncSession, instructor_id: int, instructor: InstructorCreate) -> Optional[InstructorResponse]:
    result = await db.execute(select(Instructor).where(Instructor.id == instructor_id))
    existing_instructor = result.scalars().first()
    if not existing_instructor:
        return None

    existing_instructor.name = instructor.name
    existing_instructor.bio = instructor.bio

    await db.commit()
    await db.refresh(existing_instructor)
    return existing_instructor


async def delete_instructor(db: AsyncSession, instructor_id: int) -> bool:
    result = await db.execute(select(Instructor).where(Instructor.id == instructor_id))
    existing_instructor = result.scalars().first()
    if not existing_instructor:
        return False

    await db.delete(existing_instructor)
    await db.commit()
    return True