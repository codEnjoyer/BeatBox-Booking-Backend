from pydantic import constr, EmailStr

from src.domain.schemas.base import BaseSchema
from src.domain.schemas.phone_number import PhoneNumber


class BaseUser(BaseSchema):
    email: EmailStr


class UserCredentials(BaseUser):
    password: constr(max_length=200)


# TODO: кажется, стоит переосмыслить схемы. сейчас решил ничего не трогать


class UserCreate(BaseUser):
    phone_number: PhoneNumber
    password: constr(max_length=200)
    is_superuser: bool = False


class UserRead(BaseUser):
    id: int
    is_superuser: bool = False


class UserUpdate(BaseUser):
    phone_number: PhoneNumber
