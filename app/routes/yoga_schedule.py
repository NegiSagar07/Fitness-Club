"""
This route module defines the api endpoints for managing yoga schedules in the fitness club application. 
It includes routes for creating, reading, updating, and deleting yoga schedules.
Each route interacts with the corresponding CRUD operations defined in the app.crud.yoga_schedule module to perform 
the necessary database operations. The routes are designed to handle HTTP requests and return appropriate responses based 
on the success or failure of the operations. The endpoints are structured to follow RESTful conventions, 
making it easy for clients to interact with the API.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session
from app.crud.yoga_schedule import create_yoga_schedule, get_yoga_schedule_by_id, update_yoga_schedule, delete_yoga_schedule
from app.schema import ScheduleCreate, ScheduleResponse, ScheduleUpdate


router = APIRouter(prefix="/schedules", tags=["Yoga Schedules"])

@router.post("/", response_model=ScheduleResponse)
async def create_schedule(schedule: ScheduleCreate, db: AsyncSession = Depends(get_db_session)):
    new_schedule = await create_yoga_schedule(db, schedule)
    return new_schedule


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def read_schedule(schedule_id: int, db: AsyncSession = Depends(get_db_session)):
    schedule = await get_yoga_schedule_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Yoga schedule not found")
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(schedule_id: int, schedule_update: ScheduleUpdate, db: AsyncSession = Depends(get_db_session)):
    updated_schedule = await update_yoga_schedule(db, schedule_id, schedule_update)
    if not updated_schedule:
        raise HTTPException(status_code=404, detail="Yoga schedule not found")
    return updated_schedule


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: int, db: AsyncSession = Depends(get_db_session)):
    success = await delete_yoga_schedule(db, schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Yoga schedule not found")
    return {"detail": "Yoga schedule deleted successfully"}

