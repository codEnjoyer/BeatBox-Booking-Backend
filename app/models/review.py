import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    DateTime,
    Integer,
    CheckConstraint,
    ForeignKey,
    func,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models import Room, User, Studio


class Review(BaseModel):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    text: Mapped[Optional[str]] = mapped_column(Text(1024), nullable=True)
    grade: Mapped[int] = mapped_column(
        Integer, CheckConstraint('grade > 0 AND grade <= 5'), nullable=False
    )
    published_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    room_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"), nullable=True
    )
    studio_id: Mapped[int] = mapped_column(
        ForeignKey("studios.id", ondelete="CASCADE"), nullable=False
    )

    author: Mapped["User"] = relationship(
        back_populates="reviews", lazy="joined"
    )
    room: Mapped[Optional["Room"]] = relationship(back_populates="reviews")
    studio: Mapped["Studio"] = relationship(back_populates="reviews")

    def is_written_by(self, user_id: int) -> bool:
        return self.author_id == user_id
