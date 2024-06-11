import uuid

from pydantic import HttpUrl

from src.domain.schemas.base import BaseSchema
from src.domain.models.file import SupportedFileExtensions


class BaseFile(BaseSchema): ...


class FileCreate(BaseFile):
    name: uuid.UUID
    extension: SupportedFileExtensions


class FileUpdate(BaseFile): ...


class FileRead(BaseFile):
    name: str
    extension: str
    url: HttpUrl


class FileModelRead(BaseFile):
    name: str
    extension: str  # TODO: change to enum
