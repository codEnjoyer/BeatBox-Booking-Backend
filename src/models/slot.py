from datetime import datetime

from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db import Base


class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    studio: Mapped["Studio"] = relationship(back_populates="slots", lazy="joined")
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)
    tenant: Mapped["User"] = relationship(back_populates="reserved_slots")