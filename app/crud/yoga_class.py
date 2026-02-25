"""
This module contains CRUD operations for the YogaClass model.
We will implement the following functions:
- create_yoga_class(db: AsyncSession, yoga_class: YogaClassCreate) -> YogaClassResponse
- get_yoga_class_by_id(db: AsyncSession, yoga_class_id) -> Optional[YogaClassResponse]
- update_yoga_class(db: AsyncSession, yoga_class_id, yoga_class: YogaClassUpdate) -> Optional[YogaClassResponse]
- delete_yoga_class(db: AsyncSession, yoga_class_id) -> bool
"""


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models import YogaClass
from app.schema import YogaClassCreate, YogaClassResponse, YogaClassUpdate
from typing import Optional


async def create_yoga_class(db: AsyncSession, yoga_class: YogaClassCreate) -> YogaClassResponse:
    new_yoga_class = YogaClass(
        name=yoga_class.name,
        description=yoga_class.description
    )
    db.add(new_yoga_class)
    await db.commit()
    await db.refresh(new_yoga_class)
    return new_yoga_class


async def get_yoga_class_by_id(db: AsyncSession, yoga_class_id: int) -> Optional[YogaClassResponse]:
    result = await db.execute(select(YogaClass).where(YogaClass.id == yoga_class_id))
    yoga_class = result.scalars().first()
    return yoga_class


async def update_yoga_class(db: AsyncSession, yoga_class_id: int, yoga_class: YogaClassUpdate) -> Optional[YogaClassResponse]:
    result = await db.execute(select(YogaClass).where(YogaClass.id == yoga_class_id))
    existing_yoga_class = result.scalars().first()
    if not existing_yoga_class:
        return None
    
    existing_yoga_class.name = yoga_class.name
    existing_yoga_class.description = yoga_class.description
    await db.commit()
    await db.refresh(existing_yoga_class)
    return existing_yoga_class


async def delete_yoga_class(db: AsyncSession, yoga_class_id: int) -> bool:
    result = await db.execute(select(YogaClass).where(YogaClass.id == yoga_class_id))
    existing_yoga_class = result.scalars().first()
    if not existing_yoga_class:
        return False    
    
    await db.delete(existing_yoga_class)
    await db.commit()
    return True