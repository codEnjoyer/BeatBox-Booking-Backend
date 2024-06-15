from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    # from src.domain.models.booking import Booking
    from src.domain.models.employee import Employee

    # from src.domain.models.review import Review


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=false()
    )

    employee: Mapped[Optional["Employee"]] = relationship(
        back_populates="user", lazy="joined"
    )
    # bookings: Mapped[list["Booking"]] = relationship(back_populates="user")
    # reviews: Mapped[list["Review"]] = relationship(
    #     back_populates="author", cascade="all, delete-orphan"
    # )

    def can_manage_studio(self, studio_id: int) -> bool:
        return (
            self.employee and self.employee.studio_id == studio_id
        ) or self.is_superuser
