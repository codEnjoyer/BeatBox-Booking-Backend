from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
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
        if await self.is_already_exist_with_name(schema.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Studio with same name already exists",
            )
        return await self.create(schema)

    async def is_already_exist_with_name(self, name: str) -> bool:
        try:
            _ = await self._repository.get_one(self.model.name == name)
        except NoResultFound:
            return False
        return True

    async def update(self, studio_id: int, schema: StudioUpdate) -> Studio:
        if not await self.is_already_exist_with_id(studio_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Studio with that name not found",
            )
        return await self.update_by_id(schema, studio_id)

    async def delete(self, studio_id: int, user_id: int) -> None:
        studio: Studio = await self.get_by_id(
            studio_id, options=(selectinload(Studio.employees))
        )
        # TODO: добавить обработку ошибки при отсутствии

        if any(user_id == employee.user_id for employee in studio.employees):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid permissions",
            )
        return await self.delete_by_id(studio.id)
