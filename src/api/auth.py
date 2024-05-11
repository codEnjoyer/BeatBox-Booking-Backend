from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from starlette import status
from datetime import timedelta

from src.api.dependencies.auth import get_user_by_name, manager, JsonRpcRequest
from src.database.actions import create_user
from src.domain.dependencies.auth import verify_password
from src.domain.db import get_async_session
from src.domain.schemas.auth import Token
from src.domain.schemas.user import UserAuthSchema, UserReadSchema, UserCreateSchema
from src.domain.models.user import User

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=Token)
async def auth_user(request: JsonRpcRequest,
                    session: AsyncSession = Depends(get_async_session)) -> Token:
    method_name = request.method
    params = request.params

    if method_name != "auth_user":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Method not found")

    try:
        user_schema = UserAuthSchema(**params)
        user = await get_user_by_name(user_schema.username, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username")

        if not verify_password(user_schema.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        access_token = manager.create_access_token(data=dict(sub=user_schema.username), expires=timedelta(hours=48))
        return Token(access_token=access_token, token_type='bearer')
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")


@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def register(request: JsonRpcRequest,
                   session: AsyncSession = Depends(get_async_session)) -> UserReadSchema:
    method_name = request.method
    params = request.params

    if method_name != "register":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Method not found")

    try:
        user_schema = UserCreateSchema(**params)
        user = await create_user(user_schema=user_schema, session=session)
        return UserReadSchema(id=user.id, username=user.username, email=user.email,
                              is_active=user.is_active, is_superuser=user.is_superuser)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


@router.get("/protected")
def protected_route(user: User = Depends(manager)):
    return {"message": "This is a protected route", "user": user}
