from typing import TYPE_CHECKING, Optional
import datetime as dt

from furl import furl
from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy_utils import URLType, PhoneNumber, PhoneNumberType

from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    from src.domain.models.review import Review
    from src.domain.models.room import Room
    from src.domain.models.employee import Employee


class Studio(BaseModel):
    __tablename__ = "studios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )

    address: Mapped[str] = mapped_column(String(200), nullable=False)
    latitude: Mapped[float] = mapped_column(Float(precision=8), nullable=False)
    longitude: Mapped[float] = mapped_column(Float(precision=8), nullable=False)

    opening_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    closing_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    site_url: Mapped[Optional[furl]] = mapped_column(URLType, nullable=True)
    contact_phone_number: Mapped[Optional[PhoneNumber]] = mapped_column(
        PhoneNumberType(region="RU"), nullable=True
    )
    tg: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    vk: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    whats_app: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="studio", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="studio", lazy="joined", cascade="all, delete-orphan"
    )
    rooms: Mapped[list["Room"]] = relationship(
        back_populates="studio", cascade="all, delete-orphan"
    )

    @hybrid_property
    def average_grade(self):
        return sum([review.grade for review in self.reviews]) / len(
            self.reviews
        )
