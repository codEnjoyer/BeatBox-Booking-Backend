import typing

from pydantic import EmailStr, Field

from src.domain.schemas.base import BaseSchema, IntID


class BaseUser(BaseSchema):
    email: EmailStr


class UserRead(BaseUser):
    id: IntID
    is_superuser: bool
    employee: typing.Optional["EmployeeRead"]


class UserCreate(BaseUser):
    password: str = Field(..., min_length=8, max_length=24)


class UserUpdate(BaseUser): ...


from src.domain.schemas.employee import EmployeeRead

UserRead.update_forward_refs()
