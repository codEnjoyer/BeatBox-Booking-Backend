import typing

from pydantic import EmailStr, Field, model_validator

from src.domain.schemas.base import BaseSchema, IntID, NonEmptyString


class BaseUser(BaseSchema):
    email: EmailStr


class UserRead(BaseUser):
    id: IntID
    nickname: NonEmptyString
    is_superuser: bool
    employee: typing.Optional["EmployeeRead"]


Password = typing.Annotated[str, Field(min_length=8,
                                       max_length=24,
                                       examples=["password"])]


class UserCreate(BaseUser):
    nickname: NonEmptyString | None
    password: Password

    @model_validator(mode="after")
    def password_is_not_email(self) -> typing.Self:
        if self.password == self.email:
            raise ValueError("Password cannot be the same as email")
        return self


class UserUpdate(BaseUser):
    nickname: NonEmptyString


class UserPasswordUpdate(BaseSchema):
    old_password: Password
    new_password: Password

    @model_validator(mode="after")
    def different_passwords(self) -> typing.Self:
        if self.old_password == self.new_password:
            raise ValueError("Old and new passwords must be different")
        return self


from src.domain.schemas.employee import EmployeeRead

UserRead.update_forward_refs()
