from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.security import manager, verify_password
from src.db import get_async_session
from src.database.actions import get_user_by_name
from src.schemas.user import UserAuthSchema


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


router = APIRouter(prefix="/auth")


@router.post("/token", response_model=Token)
async def auth_user(
    user_schema: UserAuthSchema, session: AsyncSession = Depends(get_async_session)
) -> Token:
    try:
        user = await get_user_by_name(user_schema.username, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username")
        
        if not verify_password(user_schema.password, user.hashed_password):
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        token = manager.create_access_token(data={'sub': user.username})
        return Token(access_token=token, token_type='bearer')
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

# Переделка на JsonPrc