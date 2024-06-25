from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.base import BaseModel

if TYPE_CHECKING:
    from app.domain.models.booking import Booking
    from app.domain.models.employee import Employee
    from app.domain.models.review import Review


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str] = mapped_column(
        String(16), unique=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=false()
    )

    employee: Mapped[Optional["Employee"]] = relationship(
        back_populates="user",
        lazy="joined",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def can_manage_studio(self, studio_id: int) -> bool:
        return (
            self.employee and self.employee.studio_id == studio_id
        ) or self.is_superuser
