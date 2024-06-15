import typing

from pydantic import EmailStr, PositiveInt, Field

from src.domain.schemas.base import BaseSchema


class BaseUser(BaseSchema):
    email: EmailStr


class UserRead(BaseUser):
    id: PositiveInt
    is_superuser: bool
    employee: typing.Optional["EmployeeRead"]


class UserCredentials(BaseUser):
    password: str = Field(..., min_length=8, max_length=24)


class UserCreate(UserCredentials): ...


class UserUpdate(BaseUser): ...


from src.domain.schemas.employee import EmployeeRead

UserRead.update_forward_refs()
