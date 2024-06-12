from typing import override

from sqlalchemy import ColumnElement
from sqlalchemy.exc import NoResultFound

from src.domain.models import Studio
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.studio import StudioCreate, StudioUpdate


class StudioRepository(
    SQLAlchemyRepository[Studio, StudioCreate, StudioUpdate]
):
    @override
    @property
    def model(self) -> type[Studio]:
        return Studio

    async def is_studio_exist(self, *where: ColumnElement[bool]) -> bool:
        try:
            await self.get_one(*where)
        except NoResultFound:
            return False
        return True
