from datetime import datetime

from sqlalchemy import DateTime, String, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author: Mapped["User"] = relationship(back_populates="reviews", lazy='joined')
    studio: Mapped["Studio"] = relationship(back_populates="reviews", lazy='joined')
    date: Mapped[str] = mapped_column(DateTime, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    text: Mapped[str] = mapped_column(String(500))
    grade: Mapped[int] = mapped_column(Integer(), CheckConstraint('grade > 0 AND grade <= 5'))
