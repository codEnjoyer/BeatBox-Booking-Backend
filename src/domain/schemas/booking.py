import datetime as dt
import uuid

from src.domain.schemas.base import BaseSchema
from src.domain.models.booking import BookingStatus


class BaseBooking(BaseSchema):
    name: str
    surname: str | None
    starts_at: dt.datetime
    ends_at: dt.datetime

    # TODO: starts_at > ends_at
    # TODO: check for minutes 00 or 30


class BookingRead(BaseBooking):
    id: uuid.UUID
    user_id: int
    status: BookingStatus
    room_id: int


class BookingCreate(BaseBooking): ...


class BookingUpdate(BaseBooking): ...


# TODO: оставить только name и surname?
