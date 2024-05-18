from pydantic import BaseModel, constr


class UserBaseSchema(BaseModel):
    email: str


class UserAuthSchema(UserBaseSchema):
    password: constr(max_length=200)


class UserCreateSchema(UserBaseSchema):
    phone_number: str
    password: constr(max_length=200)
    is_superuser: bool = False


class UserReadSchema(UserBaseSchema):
    id: int
    is_superuser: bool = False
