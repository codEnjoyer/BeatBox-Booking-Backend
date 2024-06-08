import enum
import uuid

from sqlalchemy import UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.base import BaseModel


class SupportedFileExtensions(enum.Enum):
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"
    JPG = 'jpg'


class File(BaseModel):
    __tablename__ = "files"

    name: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )
    extension: Mapped[SupportedFileExtensions] = mapped_column(
        Enum(SupportedFileExtensions), nullable=False
    )
