from sqlalchemy import DateTime, String, Integer, CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    author: Mapped["User"] = relationship(
        back_populates="reviews", lazy='joined', foreign_keys=[author_id]
    )

    studio_id: Mapped[int] = mapped_column(ForeignKey("studios.id"), nullable=False)
    studio: Mapped["Studio"] = relationship(
        back_populates="reviews", lazy='joined', foreign_keys=[studio_id]
    )
    date: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    text: Mapped[str] = mapped_column(String(500))
    grade: Mapped[int] = mapped_column(Integer, CheckConstraint('grade > 0 AND grade <= 5'))
