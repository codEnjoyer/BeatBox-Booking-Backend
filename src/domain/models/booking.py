import enum
import typing

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import BaseModel

if typing.TYPE_CHECKING:
    from src.domain.models.slot import Slot
    from src.domain.models.user import User


class BookingStatus(enum.Enum):
    WAITING_FOR_PAYMENT = "waiting_for_payment"
    EXPIRED = "expired"
    CANCELED = "canceled"
    BOOKED = "booked"


class Booking(BaseModel):
    __tablename__ = "bookings"

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), nullable=False
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("slots.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )

    slot: Mapped["Slot"] = relationship(back_populates="booking")
    user: Mapped["User"] = relationship(back_populates="bookings")
