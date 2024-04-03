from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db import Base


class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    room: Mapped["Room"] = relationship(back_populates="slots", lazy="joined", foreign_keys=[room_id])

    booked_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    booked_by: Mapped["User"] = relationship(back_populates="reserved_slots", lazy="joined", foreign_keys=[booked_by_id])