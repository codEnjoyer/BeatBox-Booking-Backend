from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Integer, CheckConstraint, ForeignKey, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    from src.domain.models.user import User
    from src.domain.models.room import Room
    from src.domain.models.studio import Studio


class Review(BaseModel):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    date: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False,
                                      server_default=func.now())
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    grade: Mapped[int] = mapped_column(Integer, CheckConstraint('grade > 0 AND grade <= 5'),
                                       nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rooms.id"), nullable=True)
    studio_id: Mapped[int] = mapped_column(ForeignKey("studios.id"), nullable=False)

    author: Mapped["User"] = relationship(
        back_populates="reviews", lazy='joined', foreign_keys=[author_id]
    )
    room: Mapped[Optional["Room"]] = relationship(
        back_populates="reviews", lazy='joined', foreign_keys=[room_id]
    )
    studio: Mapped["Studio"] = relationship(
        back_populates="reviews", lazy='joined', foreign_keys=[studio_id]
    )
