from pydantic import constr, EmailStr

from src.domain.schemas.base import BaseSchema
from src.domain.schemas.phone_number import PhoneNumber


class UserBaseSchema(BaseSchema):
    email: EmailStr


class UserAuthSchema(UserBaseSchema):
    password: constr(max_length=200)


# TODO: кажется, стоит переосмыслить схемы. сейчас решил ничего не трогать


class UserCreateSchema(UserBaseSchema):
    phone_number: PhoneNumber
    password: constr(max_length=200)
    is_superuser: bool = False


class UserReadSchema(UserBaseSchema):
    id: int
    is_superuser: bool = False


class UserUpdateSchema(UserBaseSchema):
    phone_number: PhoneNumber
