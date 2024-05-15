from typing import TYPE_CHECKING, Optional
import datetime as dt

from sqlalchemy import Integer, DateTime, ForeignKey, Boolean, true
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    from src.domain.models.booking import Booking
    from src.domain.models.room import Room


class Slot(BaseModel):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=true()
    )

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)

    booking: Mapped[Optional["Booking"]] = relationship(back_populates="slot")
    room: Mapped["Room"] = relationship(
        back_populates="slots", lazy="joined", foreign_keys=[room_id]
    )
