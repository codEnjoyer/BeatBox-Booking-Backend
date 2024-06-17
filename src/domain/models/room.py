import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.domain.models.base import BaseModel
from src.domain.models.booking import BookingStatus

if TYPE_CHECKING:
    from src.domain.models.booking import Booking
    from src.domain.models.review import Review
    from src.domain.models.studio import Studio


class Room(BaseModel):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    additional_services: Mapped[str] = mapped_column(String(500), nullable=True)

    banner: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    images: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, server_default="{}"
    )

    studio_id: Mapped[int] = mapped_column(
        ForeignKey("studios.id", ondelete="CASCADE"), nullable=False
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
        lazy="selectin",
        passive_deletes=True,
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="room",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    studio: Mapped["Studio"] = relationship(
        back_populates="rooms", lazy="joined"
    )

    def is_free_at_interval(
            self, from_: datetime.datetime, to: datetime.datetime
    ) -> bool:
        for booking in self.bookings:
            if (booking.is_within_range(from_, to)
                    and booking.status != BookingStatus.CANCELED):
                return False
        return True
