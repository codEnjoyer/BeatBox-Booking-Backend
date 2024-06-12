from typing import override

from sqlalchemy import ColumnElement

from src.domain.models.file import File
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.file import FileCreate, FileUpdate


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
