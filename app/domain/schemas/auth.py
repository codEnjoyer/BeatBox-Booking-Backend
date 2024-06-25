from pydantic import EmailStr

from app.domain.schemas.base import BaseSchema


class TokenData(BaseSchema):
    email: EmailStr | None


class Token(BaseSchema):
    access_token: str
    token_type: str
