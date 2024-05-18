from sqlalchemy import ColumnElement
from sqlalchemy.exc import NoResultFound

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
    def _model(self) -> type[Model]:
        return self._repository.model

    def __init__(
        self, repository: Repository, not_found_exception: type[NoResultFound]
    ):
        super().__init__(repository)
        self._not_found_exception = not_found_exception

    async def create(self, schema: CreateSchema, *args, **kwargs) -> Model:
        return await self._repository.create(schema)

    async def get_all(
        self, *where: ColumnElement[bool], offset: int = 0, limit: int = 100
    ) -> list[Model]:
        return await self._repository.get_all(
            *where, offset=offset, limit=limit
        )

    async def get_by_id(self, model_id: int) -> Model:
        try:
            model = await self._repository.get_one(self._model.id == model_id)
        except NoResultFound as e:
            raise self._not_found_exception from e
        return model

    # NOTE: По необходимости добавляйте этот метод в конкретный сервис модели, у которой есть name  # noqa: E501
    # async def get_by_name(self,
    #                       model_name: str) -> Model | None:
    #     try:
    #         model = await self._repository.get_one(self._model.name == model_name)  # noqa: E501
    #     except NoResultFound as e:
    #         raise self._not_found_exception from e
    #     return model

    async def update_by_id(self, schema: UpdateSchema, model_id: int) -> Model:
        try:
            model = await self._repository.update(
                schema, self._model.id == model_id
            )
        except NoResultFound as e:
            raise self._not_found_exception from e
        return model

    async def delete_by_id(self, model_id: int) -> None:
        try:
            await self._repository.delete(self._model.id == model_id)
        except NoResultFound as e:
            raise self._not_found_exception from e
