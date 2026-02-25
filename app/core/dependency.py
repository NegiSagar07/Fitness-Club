from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from .security import oauth2_scheme
from app.database import get_db_session
from .config import settings
from app.crud.user import get_user_by_id

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)): 

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credential",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
   
    user = await get_user_by_id(db, int(user_id)) 
    if user is None:
        raise credential_exception
    
    return user

