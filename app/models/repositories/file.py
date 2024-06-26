from typing import override

from models.file import File
from schemas.file import FileCreate, FileUpdate
from sqlalchemy import ColumnElement

from models.repositories.SQLAlchemy import SQLAlchemyRepository


class FileRepository(SQLAlchemyRepository[File, FileCreate, FileUpdate]):
    @override
    @property
    def model(self) -> type[File]:
        return File

    @override
    async def update(
        self, schema: FileUpdate | dict[str, ...], *where: ColumnElement[bool]
    ) -> File:
        raise NotImplementedError('Method must not be called')
