from pydantic import BaseModel, constr, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

class UserBaseSchema(BaseModel):
    email: EmailStr


class UserAuthSchema(UserBaseSchema):
    password: str = Field(..., min_length=6, max_length=200)


# PhoneNumber.phone_format = "E164"
# PhoneNumber.supported_regions = ["RU"] ## TODO: create phone number schema
# PhoneNumber.default_region_code = "RU"

class UserCreateSchema(UserBaseSchema):
    phone_number: PhoneNumber
    password: constr(max_length=200)
    is_superuser: bool = False


class UserReadSchema(UserBaseSchema):
    id: int
    is_superuser: bool = False
