import datetime as dt
import enum
import typing
import uuid

from sqlalchemy import ForeignKey, Enum, String, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if typing.TYPE_CHECKING:
    from models import Room, User


class BookingStatus(enum.Enum):
    CLOSED = "closed"
    # WAITING_FOR_PAYMENT = "waiting_for_payment"
    # EXPIRED = "expired"
    CANCELLED = "cancelled"
    BOOKED = "booked"


class Booking(BaseModel):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), nullable=False
    )
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    surname: Mapped[str] = mapped_column(String(64), nullable=True)
    starts_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ends_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    room: Mapped["Room"] = relationship(
        back_populates="bookings",
        lazy="joined",
    )
    user: Mapped["User"] = relationship(
        back_populates="bookings",
        lazy="joined",
    )

    def is_within_range(self, from_: dt.datetime, to: dt.datetime) -> bool:
        return self.starts_at <= to and self.ends_at >= from_

    def is_owned_by(self, user_id: int) -> bool:
        return self.user_id == user_id
