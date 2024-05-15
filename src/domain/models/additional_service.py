from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import BaseModel

if TYPE_CHECKING:
    from src.domain.models.room import Room


class AdditionalService(BaseModel):
    __tablename__ = "additional_services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    room: Mapped["Room"] = relationship(back_populates="additional_services")
