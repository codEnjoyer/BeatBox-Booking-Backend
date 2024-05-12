from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PhoneNumber, PhoneNumberType

from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    from src.domain.models.booking import Booking
    from src.domain.models.review import Review


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    phone_number: Mapped[PhoneNumber] = mapped_column(PhoneNumberType(region="RU"), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False,
                                               server_default=false())
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="user"
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
