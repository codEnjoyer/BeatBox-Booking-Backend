import enum
import uuid

from sqlalchemy import String, UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ChoiceType

from src.domain.models.base import BaseModel


class SupportedFileExtensions(enum.Enum):
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"


class File(BaseModel):
    __tablename__ = "files"

    name: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    extension: Mapped[SupportedFileExtensions] = mapped_column(Enum(SupportedFileExtensions),
                                                               nullable=False)
