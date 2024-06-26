from pydantic import EmailStr

from schemas.base import BaseSchema


class TokenData(BaseSchema):
    email: EmailStr | None


class Token(BaseSchema):
    access_token: str
    token_type: str
