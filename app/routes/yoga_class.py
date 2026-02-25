"""
This route module defines the API endpoints for managing yoga classes in the fitness club application. 
It includes routes for creating, retrieving, updating, and deleting yoga classes. Each route interacts with 
the corresponding CRUD operations defined in the app.crud.yoga_class module and uses the schemas defined in app.schema 
for request validation and response formatting. The routes are designed to be asynchronous and follow RESTful conventions 
for resource management.
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.yoga_class import create_yoga_class, get_yoga_class_by_id, update_yoga_class, delete_yoga_class
from app.schema import YogaClassCreate, YogaClassResponse, YogaClassUpdate
from app.database import get_db_session     


router = APIRouter(prefix="/yoga-classes", tags=["yoga-classes"])


@router.post("/", response_model=YogaClassResponse, status_code=status.HTTP_201_CREATED)
async def create_yoga_class_endpoint(yoga_class: YogaClassCreate, db: AsyncSession = Depends(get_db_session)):
    return await create_yoga_class(db, yoga_class)


@router.get("/{yoga_class_id}", response_model=YogaClassResponse)
async def get_yoga_class_endpoint(yoga_class_id: int, db: AsyncSession = Depends(get_db_session)):
    yoga_class = await get_yoga_class_by_id(db, yoga_class_id)
    if not yoga_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Yoga class not found")
    return yoga_class


@router.put("/{yoga_class_id}", response_model=YogaClassResponse)
async def update_yoga_class_endpoint(yoga_class_id: int, yoga_class: YogaClassUpdate, db: AsyncSession = Depends(get_db_session)):
       
    updated_yoga_class = await update_yoga_class(db, yoga_class_id, yoga_class)
    if not updated_yoga_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Yoga class not found")
    return updated_yoga_class


@router.delete("/{yoga_class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_yoga_class_endpoint(yoga_class_id: int, db: AsyncSession = Depends(get_db_session)):
    
    success = await delete_yoga_class(db, yoga_class_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Yoga class not found")
    return None  # No content to return after successful deletion


