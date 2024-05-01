from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.db import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))

    studio_id: Mapped[int] = mapped_column(ForeignKey("studios.id"), nullable=False)
    studio: Mapped["Studio"] = relationship(
        back_populates="rooms", lazy="joined", foreign_keys=[studio_id]
    )

    slots: Mapped[list["Slot"]] = relationship(back_populates="room", cascade="all, delete-orphan")
