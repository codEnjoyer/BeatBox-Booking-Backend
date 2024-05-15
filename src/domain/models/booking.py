import enum
import typing
import datetime as dt
import uuid

from sqlalchemy import ForeignKey, Enum, String, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import BaseModel

if typing.TYPE_CHECKING:
    from src.domain.models.room import Room
    from src.domain.models.user import User


class BookingStatus(enum.Enum):
    CLOSED = "closed"
    WAITING_FOR_PAYMENT = "waiting_for_payment"
    EXPIRED = "expired"
    CANCELED = "canceled"
    BOOKED = "booked"


class Booking(BaseModel):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    starts_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ends_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="slots", lazy="joined")
    user: Mapped["User"] = relationship(
        back_populates="bookings", lazy="joined"
    )
