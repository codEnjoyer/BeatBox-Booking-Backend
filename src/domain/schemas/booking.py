import datetime
import uuid

from pydantic import PositiveInt

from src.domain.schemas.base import BaseSchema
from src.domain.models.booking import BookingStatus


class BaseBooking(BaseSchema):
    name: str
    surname: str | None


class BookingRead(BaseBooking):
    id: uuid.UUID
    status: BookingStatus

    user: "UserRead"
    room_id: PositiveInt

    starts_at: datetime.datetime
    ends_at: datetime.datetime
    # TODO: starts_at > ends_at
    # TODO: check for minutes 00 or 30


class BookingCreate(BaseBooking):
    starts_at: datetime.datetime
    ends_at: datetime.datetime

    # TODO: starts_at > ends_at
    # TODO: check for minutes 00 or 30


class BookingUpdate(BaseBooking): ...


from src.domain.schemas.user import UserRead

BookingRead.update_forward_refs()
