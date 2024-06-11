from fastapi import HTTPException
from starlette import status

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

    async def create(self, schema: StudioCreate, **kwargs) -> Studio:
        if await self._repository.is_studio_exist(
            self._model.name == schema.name
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Studio with same name already exists",
            )
        return await self._repository.create(schema=schema)

    async def delete(self, studio_id: int, user_id: int) -> None:
        if not await self._repository.is_studio_exist(
            self._model.id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Studio with that name not found",
            )

        studio: Studio = await self._repository.get(
            user_id, self._model.id == studio_id
        )
        return await self._repository.delete(self._model.id == studio.id)

    async def update(
        self, studio_id: int, user_id: int, schema: StudioUpdate
    ) -> Studio:
        if not await self._repository.is_studio_exist(
            self._model.id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Studio with that name not found",
            )
        studio: Studio = await self._repository.get(
            user_id, self._model.id == studio_id
        )
        return await self._repository.update_one(
            schema, self._model.id == studio.id
        )
