"""
This routes module defines the API endpoints for managing yoga sessions in the fitness club application.
It includes endpoints for creating, retrieving, updating, and deleting yoga sessions. Each endpoint interacts with 
the corresponding CRUD operations defined in the app.crud.yoga_session module to perform the necessary database operations.
The routes are designed to handle HTTP requests and return appropriate responses based on the success or failure of 
the operations. The endpoints are structured to follow RESTful conventions, making it easy for clients to interact with the API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session
from app.crud.yoga_session import create_yoga_session, get_yoga_session_by_id, update_yoga_session, delete_yoga_session
from app.schema import YogaSessionCreate, YogaSessionResponse, YogaSessionUpdate


router = APIRouter(prefix="/yoga_sessions", tags=["Yoga Sessions"])

@router.post("/", response_model=YogaSessionResponse)
async def create_session(session: YogaSessionCreate, db: AsyncSession = Depends(get_db_session)):
    new_session = await create_yoga_session(db, session)
    return new_session


@router.get("/{session_id}", response_model=YogaSessionResponse)
async def read_session(session_id: int, db: AsyncSession = Depends(get_db_session)):
    session = await get_yoga_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Yoga session not found")
    return session


@router.put("/{session_id}", response_model=YogaSessionResponse)
async def update_session(session_id: int, session_update: YogaSessionUpdate, db: AsyncSession = Depends(get_db_session)):
    updated_session = await update_yoga_session(db, session_id, session_update)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Yoga session not found")
    return updated_session


@router.delete("/{session_id}")
async def delete_session(session_id: int, db: AsyncSession = Depends(get_db_session)):
    success = await delete_yoga_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Yoga session not found")
    return {"detail": "Yoga session deleted successfully"}


