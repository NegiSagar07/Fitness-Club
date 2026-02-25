"""
This routes module defines the API endpoints for managing bookings in the fitness club application.
It includes endpoints for creating, retrieving, updating, and deleting bookings. Each endpoint interacts with
the corresponding CRUD operations defined in the app.crud.booking module to perform the necessary database operations.
The routes are designed to handle HTTP requests and return appropriate responses based on the success or failure of
the operations. The endpoints are structured to follow RESTful conventions, making it easy for clients to interact with the API.
Only authenticated users can create, update, or delete bookings, while anyone can retrieve booking information.
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.yoga_session import get_yoga_session_by_id
from app.database import get_db_session
from app.crud.booking import create_booking, get_booking_by_id, update_booking, delete_booking
from app.schema import BookingCreate, BookingResponse, BookingUpdate
from app.core.dependency import get_current_user


router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_new_booking(booking: BookingCreate, db: AsyncSession = Depends(get_db_session), current_user=Depends(get_current_user)):
    # before creating a booking, make sure the session_id provided in the booking exists and is valid, and the session has available slots
    db_session = await get_yoga_session_by_id(db, booking.session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Yoga session not found")
    if db_session.max_capacity <= db_session.current_bookings:
        raise HTTPException(status_code=400, detail="Yoga session is fully booked")

    # Both the session increment and booking creation happen atomically in the CRUD function
    # If booking creation fails, the increment is automatically rolled back
    new_booking = await create_booking(db, booking, current_user.id, db_session)
    
    return new_booking


@router.get("/{booking_id}", response_model=BookingResponse)
async def read_booking(booking_id: int, db: AsyncSession = Depends(get_db_session)):
    booking = await get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_existing_booking(booking_id: int, booking_update: BookingUpdate, db: AsyncSession = Depends(get_db_session), current_user=Depends(get_current_user)):
    existing_booking = await get_booking_by_id(db, booking_id)
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if existing_booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this booking")
    
    updated_booking = await update_booking(db, booking_id, booking_update)
    return updated_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_booking(booking_id: int, db: AsyncSession = Depends(get_db_session), current_user=Depends(get_current_user)):
    existing_booking = await get_booking_by_id(db, booking_id)
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if existing_booking.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this booking")
    
    success = await delete_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return None  # 204 No Content does not return a body


