from pydantic import constr

from src.domain.schemas.base import BaseSchema


class UserBaseSchema(BaseSchema):
    email: str


class UserAuthSchema(UserBaseSchema):
    password: constr(max_length=200)


# TODO: кажется, стоит переосмыслить схемы. сейчас решил ничего не трогать

class UserCreateSchema(UserBaseSchema):
    phone_number: str
    password: constr(max_length=200)
    is_superuser: bool = False


class UserReadSchema(UserBaseSchema):
    id: int
    is_superuser: bool = False


class UserUpdateSchema(UserBaseSchema):
    phone_number: str
