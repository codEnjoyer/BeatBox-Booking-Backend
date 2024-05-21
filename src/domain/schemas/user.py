from pydantic import BaseModel, constr, EmailStr, Field

from src.domain.dependencies.phone_number import PhoneNumber


class UserBaseSchema(BaseModel):
    email: EmailStr


class UserAuthSchema(UserBaseSchema):
    password: str = Field(..., min_length=6, max_length=200)




class UserCreateSchema(UserBaseSchema):
    phone_number: PhoneNumber = Field(..., example="+79876543210")
    password: constr(max_length=200)
    # is_superuser: bool = False


class UserReadSchema(UserBaseSchema):
    id: int
    is_superuser: bool = False
