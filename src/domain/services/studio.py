from sqlalchemy import ColumnElement
from sqlalchemy.exc import NoResultFound

from src.domain.exceptions.studio import StudioNotFoundException
from src.domain.models.repositories.studio import StudioRepository
from src.domain.schemas.studio import StudioCreate, StudioUpdate
from src.infrastructure.service import Service
from src.models import Studio


class StudioService(Service[StudioRepository]):

    def __init__(self):
        super().__init__(StudioRepository)

    async def create(self,
                     schema: StudioCreate) -> Studio:
        return await self._repository.create(schema)

    async def get_all(self,
                      *where: ColumnElement[bool],
                      offset: int = 0,
                      limit: int = 100) -> list[Studio]:
        return await self._repository.get_all(*where,
                                              offset=offset,
                                              limit=limit)

    async def get_by_id(self,
                        studio_id: int) -> Studio:
        try:
            studio = await self._repository.get_one(Studio.id == studio_id)
        except NoResultFound as e:
            raise StudioNotFoundException from e
        return studio

    async def get_by_name(self,
                          studio_name: str) -> Studio | None:
        try:
            studio = await self._repository.get_one(Studio.name == studio_name)
        except NoResultFound as e:
            raise StudioNotFoundException from e
        return studio

    async def update_by_id(self,
                           schema: StudioUpdate,
                           studio_id: int) -> Studio:
        try:
            studio = await self._repository.update(schema, Studio.id == studio_id)
        except NoResultFound as e:
            raise StudioNotFoundException from e
        return studio

    async def delete_by_id(self,
                           studio_id: int) -> None:
        try:
            await self._repository.delete(Studio.id == studio_id)
        except NoResultFound as e:
            raise StudioNotFoundException from e
