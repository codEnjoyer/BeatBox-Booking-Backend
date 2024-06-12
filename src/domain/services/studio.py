from fastapi import HTTPException
from sqlalchemy.orm import selectinload
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
                self.model.name == schema.name
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Studio with same name already exists",
            )
        return await self._repository.create(schema)

    async def delete(self, studio_id: int, user_id: int) -> None:
        if not await self._repository.is_studio_exist(
                self.model.id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Studio with that name not found",
            )

        studio: Studio = await self.get_by_id(studio_id,
                                              options=(selectinload(
                                                  Studio.employees))
                                              )
        if any(user_id == employee.user_id for employee in studio.employees):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid permissions",
            )
        return await self._repository.delete(self.model.id == studio.id)

    async def update(self, studio_id: int, schema: StudioUpdate) -> Studio:
        if not await self._repository.is_studio_exist(
                self.model.id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Studio with that name not found",
            )
        return await self.update_by_id(schema, studio_id)
