from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from starlette import status

from src.api.dependencies.auth import get_user_by_name, manager
from src.database.actions import create_user
from src.domain.dependencies.auth import verify_password
from src.domain.db import get_async_session
from src.domain.schemas.auth import Token
from src.domain.schemas.user import UserAuthSchema, UserReadSchema, UserCreateSchema

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=Token)
async def auth_user(user_schema: UserAuthSchema,
                    session: AsyncSession = Depends(get_async_session)) -> Token:
    try:
        user = await get_user_by_name(user_schema.username, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username")

        if not verify_password(user_schema.password, user.hashed_password):
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        token = manager.create_access_token(data={'sub': user.username})
        return Token(access_token=token, token_type='bearer')
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")


# Переделка на JsonPrc
@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def register(user_schema: UserCreateSchema,
                   session: AsyncSession = Depends(get_async_session)) -> UserReadSchema:
    try:
        user = await create_user(user_schema=user_schema, session=session)
        return UserReadSchema(id=user.id, username=user.username, email=user.email,
                              is_active=user.is_active, is_superuser=user.is_superuser)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
