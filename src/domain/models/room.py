import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.domain.models.additional_service import AdditionalService
from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    from src.domain.models.booking import Booking
    from src.domain.models.file import File
    from src.domain.models.review import Review
    from src.domain.models.studio import Studio


class Room(BaseModel):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500))

    banner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("files.name"), nullable=True
    )
    studio_id: Mapped[int] = mapped_column(
        ForeignKey("studios.id"), nullable=False
    )

    additional_services: Mapped[list["AdditionalService"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )
    banner: Mapped[Optional["File"]] = relationship(
        lazy="joined", foreign_keys=[banner_id]
    )
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="room", cascade="all, delete-orphan", lazy="selectin"
    )
    images: Mapped[list["File"]] = relationship(
        secondary="room_images", cascade="all"
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="room", lazy="joined", cascade="all, delete-orphan"
    )
    studio: Mapped["Studio"] = relationship(
        back_populates="rooms", lazy="joined", foreign_keys=[studio_id]
    )


class RoomImage(BaseModel):
    __tablename__ = "room_images"

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"), primary_key=True
    )
    image_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("files.name"), primary_key=True
    )
