from typing import Annotated

from pydantic import Field

from app.domain.schemas.base import BaseSchema, IntID, NonEmptyString

from app.domain.schemas.booking import BookingRead


class BaseRoom(BaseSchema):
    name: Annotated[NonEmptyString, Field(max_length=100)]
    description: Annotated[NonEmptyString, Field(max_length=1024)] | None
    equipment: Annotated[NonEmptyString, Field(max_length=512)] | None
    additional_services: Annotated[NonEmptyString, Field(max_length=512)] | None


class RoomRead(BaseRoom):
    id: IntID

    bookings: list[BookingRead]


class RoomCreate(BaseRoom): ...


class RoomUpdate(BaseRoom): ...
