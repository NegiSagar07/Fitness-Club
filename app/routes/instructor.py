"""
This is the route module for handling instructor-related API endpoints. 
It defines the necessary routes for creating, retrieving, updating, and deleting instructors in the fitness club 
application. The routes will interact with the CRUD operations defined in the app.crud.instructor module and use 
the Instructor schema for request and response validation. Each route will be designed to handle asynchronous requests 
and provide appropriate HTTP status codes and responses based on the outcome of the operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.instructor import create_instructor, get_instructor_by_id, update_instructor, delete_instructor
from app.schema import InstructorCreate, InstructorResponse
from app.database import get_db_session


router = APIRouter(prefix="/instructors", tags=["instructors"])

@router.post("/", response_model=InstructorResponse, status_code=status.HTTP_201_CREATED)
async def create_instructor_endpoint(instructor: InstructorCreate, db: AsyncSession = Depends(get_db_session)):
    return await create_instructor(db, instructor)  


@router.get("/{instructor_id}", response_model=InstructorResponse)
async def get_instructor_endpoint(instructor_id: int, db: AsyncSession = Depends(get_db_session)):
    instructor = await get_instructor_by_id(db, instructor_id)
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return instructor


@router.put("/{instructor_id}", response_model=InstructorResponse)
async def update_instructor_endpoint(instructor_id: int, instructor: InstructorCreate, db: AsyncSession = Depends(get_db_session)):
    
    updated_instructor = await update_instructor(db, instructor_id, instructor.name, instructor.bio)
    if not updated_instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return updated_instructor


@router.delete("/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instructor_endpoint(instructor_id: int, db: AsyncSession = Depends(get_db_session)):
    
    success = await delete_instructor(db, instructor_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return None  # No content to return after successful deletion

