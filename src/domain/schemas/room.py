import uuid

from pydantic import PositiveInt, Field, HttpUrl

from src.domain.schemas.additional_service import (
    AdditionalServiceRead,
    AdditionalServiceCreate,
)
from src.domain.schemas.base import BaseSchema
from src.domain.schemas.booking import BookingRead
from src.domain.schemas.review import ReviewRead
from src.domain.schemas.studio import StudioRead


class BaseRoom(BaseSchema):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)


class RoomRead(BaseRoom):
    id: PositiveInt
    banner: HttpUrl | None
    studio: StudioRead

    images: list[HttpUrl]
    additional_services: list[AdditionalServiceRead]
    bookings: list[BookingRead]
    reviews: list[ReviewRead]


class RoomCreate(BaseRoom):
    banner_id: uuid.UUID | None
    additional_services: list[AdditionalServiceCreate]


class RoomUpdate(RoomCreate):
    banner_id: uuid.UUID | None
    # NOTE: additional_services отсутствуют намеренно
