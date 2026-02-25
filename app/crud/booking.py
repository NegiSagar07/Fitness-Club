"""
This module contains CRUD operations for the Booking model.
It provides functions to create, read, update, and delete bookings in the database.
Each function interacts with the database session to perform the necessary operations on the Booking model,
ensuring that the data is correctly managed and persisted. The functions are designed to be used in
the route handlers for managing bookings in the application.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Booking, YogaSession


async def create_booking(db: AsyncSession, booking: Booking, current_user_id: int, yoga_session: YogaSession = None) -> Booking:
    """
    Create a booking and increment the yoga session's current_bookings count atomically.
    
    Both operations are wrapped in a single transaction to ensure data consistency.
    If either operation fails, the entire transaction is rolled back.
    """
    try:
        new_booking = Booking(
            user_id=current_user_id,
            session_id=booking.session_id
        )
        db.add(new_booking)
        
        # Increment the session's booking count in the same transaction
        if yoga_session:
            yoga_session.current_bookings += 1
        
        await db.commit()
        await db.refresh(new_booking)
        return new_booking
    except Exception as e:
        # If anything fails, rollback the transaction
        await db.rollback()
        raise e


async def get_booking_by_id(db: AsyncSession, booking_id: int) -> Booking:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalars().first()
    return booking


async def update_booking(db: AsyncSession, booking_id: int, updated_booking: Booking) -> Booking:
    existing_booking = await get_booking_by_id(db, booking_id)
    if not existing_booking:
        return None
    
    existing_booking.session_id = updated_booking.session_id

    await db.commit()
    await db.refresh(existing_booking)
    return existing_booking


async def delete_booking(db: AsyncSession, booking_id: int) -> bool:
    existing_booking = await get_booking_by_id(db, booking_id)
    if not existing_booking:
        return False
    
    await db.delete(existing_booking)
    await db.commit()
    return True

