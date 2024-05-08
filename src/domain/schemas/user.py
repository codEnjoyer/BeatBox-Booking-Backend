from pydantic import BaseModel, constr


class UserAuthSchema(BaseModel):
    username: str
    password: constr(max_length=200)


class UserBaseSchema(BaseModel):
    username: str
    email: str


class UserCreateSchema(UserBaseSchema):
    password: constr(max_length=200)
    is_superuser: bool = False


class UserReadSchema(UserBaseSchema):
    id: int
    is_active: bool
    is_superuser: bool = False
