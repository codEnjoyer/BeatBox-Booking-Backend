from typing import override

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from exceptions.studio import StudioNotFoundException
from models import Studio
from models.repositories.studio import StudioRepository
from schemas.studio import StudioCreate, StudioUpdate
from services.base import ModelService


class StudioService(
    ModelService[StudioRepository, Studio, StudioCreate, StudioUpdate]
):
    def __init__(self):
        super().__init__(StudioRepository(), StudioNotFoundException)

    @override
    async def create(self, schema: StudioCreate) -> Studio:
        created = await self._repository.create(schema)
        with_reviews = await self.get_by_id(
            created.id, options=(selectinload(self.model.reviews),)
        )
        return with_reviews

    async def create_if_not_exists(self, schema: StudioCreate) -> Studio:
        try:
            return await self._repository.get_one(
                self.model.name == schema.name
            )
        except NoResultFound:
            return await self.create(schema)

    @override
    async def update_by_id(self, model_id: int, schema: StudioUpdate) -> Studio:
        updated = await super().update_by_id(model_id, schema)
        with_reviews = await self.get_by_id(
            updated.id, options=(selectinload(self.model.reviews),)
        )
        return with_reviews
