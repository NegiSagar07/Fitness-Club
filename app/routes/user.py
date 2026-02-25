"""
This module defines the FastAPI routes for managing users in the fitness club application.
It includes endpoints for creating a new user, retrieving user details, updating user information, and deleting a user.
The routes interact with the database through the CRUD operations defined in app/crud/user.py and use
Pydantic schemas from app/schema.py for request validation and response formatting.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import UserCreate, UserResponse, Token
from app.crud.user import create_user, get_user_by_email, get_user_by_id, update_user, delete_user
from app.database import get_db_session  
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Hash the password before storing it (you should implement a proper hashing function)
    hashed_password = hash_password(user.password)
    new_user = await create_user(db, user, hashed_password)
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_info(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Hash the password before updating it (you should implement a proper hashing function)
    hashed_password = hash_password(user.password)
    updated_user = await update_user(db, user_id, user, hashed_password)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(user_id: int, db: AsyncSession = Depends(get_db_session)):
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None  # 204 No Content does not return a body


@router.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    """
    Login endpoint to authenticate user and return access token.
    The tokenUrl in oauth2_scheme should match this endpoint path.
    """
    # The form_data.username contains the email in this case
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with user_id as "sub" claim
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


