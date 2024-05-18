from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PhoneNumberType

from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    from src.domain.models.booking import Booking
    from src.domain.models.employee import Employee
    from src.domain.models.review import Review


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(
        PhoneNumberType(region="RU"), nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=false()
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")
    employee: Mapped["Employee"] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
