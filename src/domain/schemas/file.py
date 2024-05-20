import uuid

from pydantic import HttpUrl

from src.domain.schemas.base import BaseSchema
from src.domain.models.file import SupportedFileExtensions


class BaseFile(BaseSchema):
    pass


class FileCreate(BaseFile):
    name: uuid.UUID
    extension: SupportedFileExtensions


class FileUpdate(BaseFile):
    pass


class FileRead(BaseFile):
    name: str
    extension: str
    url: HttpUrl


class FileModelRead(BaseFile):
    name: str
    extension: str


class FileBucketRead(BaseFile):
    url: HttpUrl
