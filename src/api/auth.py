from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from starlette import status
from datetime import timedelta

from src.api.dependencies.auth import (
    get_user_by_email,
    manager,
    AuthenticatedUser,
)
from src.database.actions import create_user
from src.domain.dependencies.auth import verify_password
from src.domain.db import get_async_session
from src.domain.schemas.auth import Token
from src.domain.schemas.user import (
    UserAuthSchema,
    UserReadSchema,
    UserCreateSchema,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(
    user_schema: UserAuthSchema,
    session: AsyncSession = Depends(get_async_session),
) -> Token:
    try:
        user = await get_user_by_email(user_schema.email, session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username",
            )

        if not verify_password(user_schema.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )

        access_token = manager.create_access_token(
            data=dict(sub=user_schema.email), expires=timedelta(hours=48)
        )
        return Token(access_token=access_token, token_type='bearer')
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )


@router.post(
    "/register",
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_schema: UserCreateSchema,
    session: AsyncSession = Depends(get_async_session),
) -> UserReadSchema:
    try:
        user = await create_user(user_schema=user_schema, session=session)
        return UserReadSchema(
            id=user.id,
            email=user.email,
            is_superuser=user.is_superuser,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )


@router.post('/token')
async def token_login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return await login(
        UserAuthSchema(email=data.username, password=data.password), session
    )


@router.get("/protected")
def protected_route(user: AuthenticatedUser):
    return {"message": "This is a protected route", "user": user}
