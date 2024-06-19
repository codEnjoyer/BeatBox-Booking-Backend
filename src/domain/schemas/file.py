from pydantic import HttpUrl

from src.domain.schemas.base import BaseSchema


class FileRead(BaseSchema):
    url: HttpUrl
    extension: str
