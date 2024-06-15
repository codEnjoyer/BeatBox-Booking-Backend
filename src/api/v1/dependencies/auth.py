from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError

from src.api.v1.dependencies.services import UserServiceDep, AuthServiceDep
from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import User, Employee

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")
BearerTokenDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2Dep = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user(token: BearerTokenDep,
                           auth_service: AuthServiceDep,
                           user_service: UserServiceDep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth_service.decode_jwt(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception from e

    try:
        user = await user_service.get_by_email(email)
    except UserNotFoundException as e:
        raise credentials_exception from e
    return user


AuthenticatedUser = Annotated[User, Depends(get_current_user)]


async def get_current_user_employee(user: AuthenticatedUser) -> Employee:
    employee: Employee | None = user.employee
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    return employee


AuthenticatedEmployee = Annotated[Employee, Depends(get_current_user_employee)]


async def get_current_superuser(user: AuthenticatedUser) -> User:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    return user


AuthenticatedSuperuser = Annotated[User, Depends(get_current_superuser)]
