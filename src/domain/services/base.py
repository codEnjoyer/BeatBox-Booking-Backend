from sqlalchemy import ColumnElement
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.base import ExecutableOption

from src.domain.models.base import BaseModel
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.base import BaseSchema
from src.infrastructure.service import Service


class ModelService[
Repository: SQLAlchemyRepository,
Model: BaseModel,
CreateSchema: BaseSchema,
UpdateSchema: BaseSchema,
](Service[Repository]):
    _not_found_exception: type[NoResultFound]

    @property
    def model(self) -> type[Model]:
        return self._repository.model

    def __init__(
            self, repository: Repository,
            not_found_exception: type[NoResultFound]
    ):
        super().__init__(repository)
        self._not_found_exception = not_found_exception

    async def create(self, schema: CreateSchema, *args, **kwargs) -> Model:
        return await self._repository.create(schema)

    async def get_all(self,
                      *where: ColumnElement[bool],
                      options: tuple[ExecutableOption] | None = None,
                      offset: int = 0,
                      limit: int = 100
                      ) -> list[Model]:
        try:
            models = await self._repository.get_all(
                *where, options=options, offset=offset, limit=limit
            )
        except NoResultFound as e:
            raise self._not_found_exception from e
        return models

    async def get_by_id(self,
                        model_id: int,
                        options: tuple[ExecutableOption] | None = None) \
            -> Model:
        try:
            model = await self._repository.get_one(self.model.id == model_id,
                                                   options=options)
        except NoResultFound as e:
            raise self._not_found_exception from e
        return model

    async def update_by_id(self, schema: UpdateSchema, model_id: int) -> Model:
        try:
            model = await self._repository.update(
                schema, self.model.id == model_id
            )
        except NoResultFound as e:
            raise self._not_found_exception from e
        return model.one()

    async def delete_by_id(self, model_id: int) -> None:
        try:
            await self._repository.delete(self.model.id == model_id)
        except NoResultFound as e:
            raise self._not_found_exception from e
