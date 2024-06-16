from typing import override

from sqlalchemy.orm import selectinload

from src.domain.exceptions.studio import StudioNotFoundException
from src.domain.models import Studio
from src.domain.models.repositories.studio import StudioRepository
from src.domain.schemas.studio import StudioCreate, StudioUpdate
from src.domain.services.base import ModelService


class StudioService(
    ModelService[StudioRepository, Studio, StudioCreate, StudioUpdate]
):
    def __init__(self):
        super().__init__(StudioRepository(), StudioNotFoundException)

    @override
    async def create(self, schema: StudioCreate, **kwargs) -> Studio:
        created = await self._repository.create(schema)
        with_reviews = await self.get_by_id(
            created.id, options=(selectinload(self.model.reviews),)
        )
        return with_reviews

    @override
    async def update_by_id(self, model_id: int, schema: StudioUpdate) -> Studio:
        updated = await super().update_by_id(model_id, schema)
        with_reviews = await self.get_by_id(
            updated.id, options=(selectinload(self.model.reviews),)
        )
        return with_reviews
