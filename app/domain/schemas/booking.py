import uuid
from typing import Self, Annotated

from pydantic import (
    model_validator,
    field_validator,
    AwareDatetime,
    Field,
    FutureDatetime,
)

from app.domain.schemas.base import (
    BaseSchema,
    IntID,
    DatetimeTZ,
    NonEmptyString,
)
from app.domain.models.booking import BookingStatus


class BaseBooking(BaseSchema):
    name: NonEmptyString
    surname: NonEmptyString | None


class BookingRead(BaseBooking):
    id: uuid.UUID
    status: BookingStatus

    user: "UserRead"
    room_id: IntID

    starts_at: DatetimeTZ
    ends_at: DatetimeTZ

    @model_validator(mode="after")
    def starts_before_ends(self) -> Self:
        if self.starts_at >= self.ends_at:
            raise ValueError("starts_at must be before ends_at")
        return self

    @field_validator("starts_at", "ends_at")
    @classmethod
    def multiples_of_30(cls, value: DatetimeTZ) -> DatetimeTZ:
        if value.minute % 30 != 0 or value.second != 0:
            raise ValueError(
                "starts_at and ends_at must be multiples of 30 minutes"
            )
        return value


class BookingCreate(BaseBooking):
    starts_at: Annotated[
        AwareDatetime,
        FutureDatetime,
        Field(examples=['2024-06-16T11:00:00+0500']),
    ]
    ends_at: Annotated[
        AwareDatetime,
        FutureDatetime,
        Field(examples=['2024-06-16T11:00:00+0500']),
    ]

    @model_validator(mode="after")
    def starts_before_ends(self) -> Self:
        if self.starts_at >= self.ends_at:
            raise ValueError("starts_at must be before ends_at")
        return self

    @field_validator("starts_at", "ends_at")
    @classmethod
    def multiples_of_30(cls, value: DatetimeTZ) -> DatetimeTZ:
        if value.minute % 30 != 0 or value.second != 0:
            raise ValueError(
                "starts_at and ends_at must be multiples of 30 minutes"
            )
        return value


class BookingUpdate(BaseBooking): ...


from app.domain.schemas.user import UserRead

BookingRead.update_forward_refs()
