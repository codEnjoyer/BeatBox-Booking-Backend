import datetime
import uuid

from src.domain.schemas.base import BaseSchema
from src.domain.models.booking import BookingStatus
from src.domain.schemas.room import RoomRead
from src.domain.schemas.user import UserRead


class BaseBooking(BaseSchema):
    name: str
    surname: str | None


class BookingRead(BaseBooking):
    id: uuid.UUID
    status: BookingStatus

    starts_at: datetime.datetime
    ends_at: datetime.datetime
    # TODO: starts_at > ends_at
    # TODO: check for minutes 00 or 30

    user: UserRead
    room: RoomRead


class BookingCreate(BaseBooking):
    starts_at: datetime.datetime
    ends_at: datetime.datetime

    # TODO: starts_at > ends_at
    # TODO: check for minutes 00 or 30


class BookingUpdate(BaseBooking):
    ...
