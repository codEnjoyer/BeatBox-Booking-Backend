from pydantic import HttpUrl

from src.domain.schemas.base import BaseSchema, IntID, NonEmptyString

from src.domain.schemas.booking import BookingRead


class BaseRoom(BaseSchema):
    name: NonEmptyString
    description: NonEmptyString | None
    additional_services: NonEmptyString | None


class RoomRead(BaseRoom):
    id: IntID
    banner: HttpUrl | None
    images: list[HttpUrl]

    bookings: list[BookingRead]


class RoomCreate(BaseRoom): ...


class RoomUpdate(BaseRoom): ...
