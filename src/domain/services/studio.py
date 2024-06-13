from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
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
        return await self._repository.create(schema)

    async def is_already_exist_with_name(self, name: str) -> bool:
        try:
            _ = await self._repository.get_one(self.model.name == name)
        except NoResultFound:
            return False
        return True
