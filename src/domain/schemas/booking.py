import datetime as dt
import uuid

from src.domain.schemas.base import BaseSchema
from src.domain.models.booking import BookingStatus


class BaseBooking(BaseSchema):
    status: BookingStatus
    name: str
    surname: str | None
    starts_at: dt.datetime
    ends_at: dt.datetime
    room_id: int


class BookingRead(BaseBooking):
    id: uuid.UUID
    user_id: int


class BookingCreate(BaseBooking):
    ...


class BookingUpdate(BaseBooking):
    ...
