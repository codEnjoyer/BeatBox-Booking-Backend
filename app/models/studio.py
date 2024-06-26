import datetime as dt
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Integer, Float, Time
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, relationship, Mapped

from models.base import BaseModel

if TYPE_CHECKING:
    from models import Employee, Review, Room


class Studio(BaseModel):
    __tablename__ = "studios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(
        String(1024), nullable=True
    )
    opening_at: Mapped[dt.time] = mapped_column(
        Time(timezone=True), nullable=False
    )
    closing_at: Mapped[dt.time] = mapped_column(
        Time(timezone=True), nullable=False
    )

    banner_filename: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )

    latitude: Mapped[float] = mapped_column(Float(precision=8), nullable=False)
    longitude: Mapped[float] = mapped_column(Float(precision=8), nullable=False)

    site: Mapped[Optional[str]] = mapped_column(String(2083), nullable=True)
    contact_phone_number: Mapped[Optional[str]] = mapped_column(
        String(16), nullable=True
    )
    tg: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    vk: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    whats_app: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="studio",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="studio",
        lazy="joined",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    rooms: Mapped[list["Room"]] = relationship(
        back_populates="studio",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @hybrid_property
    def average_grade(self) -> float:
        if not self.reviews:
            return 0
        total = sum(review.grade for review in self.reviews)
        count = len(self.reviews)  # noqa
        return total / count
