from fastapi import APIRouter, HTTPException
from starlette import status

from api.v1.dependencies.auth import OAuth2Dep
from api.v1.dependencies.services import UserServiceDep, AuthServiceDep
from exceptions.user import (
    UserNotFoundException,
    EmailAlreadyTakenException,
    NicknameAlreadyTakenException,
)
from models import User
from schemas.auth import Token
from schemas.user import UserRead, UserCreate

router = APIRouter(tags=["Auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    schema: UserCreate,
    user_service: UserServiceDep,
) -> User:
    try:
        user = await user_service.create(schema)
    except (EmailAlreadyTakenException, NicknameAlreadyTakenException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2Dep,
    user_service: UserServiceDep,
    auth_service: AuthServiceDep,
) -> dict[str, str]:
    email, password = form_data.username, form_data.password
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = await user_service.get_by_email(email)
    except UserNotFoundException as e:
        raise credentials_exception from e

    if not user_service.is_password_valid(
        plain=password, hashed=user.hashed_password
    ):
        raise credentials_exception

    token = auth_service.create_access_token(
        data={'sub': user.email},
    )
    return {"access_token": token, "token_type": "bearer"}
