from pydantic import Field, HttpUrl

from src.domain.schemas.base import BaseSchema, IntID

from src.domain.schemas.additional_service import (
    AdditionalServiceRead,
    AdditionalServiceCreate,
)
from src.domain.schemas.booking import BookingRead


class BaseRoom(BaseSchema):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)


class RoomRead(BaseRoom):
    id: IntID
    banner: HttpUrl | None

    images: list[HttpUrl]
    additional_services: list[AdditionalServiceRead]
    bookings: list[BookingRead]


class RoomCreate(BaseRoom):
    additional_services: list[AdditionalServiceCreate]


class RoomUpdate(BaseRoom):
    ...
    # NOTE: additional_services отсутствуют намеренно
