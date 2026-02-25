"""
implementation of CRUD operations for User model
we will implement the following functions:
- create_user(db: AsyncSession, name, email, hashed_password) -> UserResponse
- get_user_by_email(db: AsyncSession, email) -> Optional[UserResponse]
- get_user_by_id(db: AsyncSession, user_id) -> Optional[UserResponse]
- update_user(db: AsyncSession, user_id, name, email, hashed_password) -> Optional[UserResponse]
- delete_user(db: AsyncSession, user_id) -> bool
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models import User
from app.schema import UserCreate, UserResponse
from typing import Optional     

async def create_user(db: AsyncSession, user: UserCreate, hashed_password: str) -> UserResponse:
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return user


async def update_user(db: AsyncSession, user_id: int, user: UserCreate, hashed_password: str) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        return None

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.hashed_password = hashed_password

    await db.commit()
    await db.refresh(existing_user)
    return existing_user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        return False

    await db.delete(existing_user)
    await db.commit()
    return True


