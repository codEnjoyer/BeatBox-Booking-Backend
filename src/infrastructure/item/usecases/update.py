from src.infrastructure.exceptions import ItemNotFoundException
from src.infrastructure.item.operations import UpdateOperation
from src.infrastructure.item.repository import Repository as RepositoryABC
from src.infrastructure.item.usecase import UseCase


class UpdateItemUseCase[Item, Schema, Repository: RepositoryABC] \
            (UseCase[Repository], UpdateOperation[Item, Schema]):
    _not_found_exception: Exception

    async def update(self,
                     schema: Schema,
                     *where) -> list[Item]:
        try:
            result = await self._repository.update(schema, *where)
        except ItemNotFoundException as e:
            raise self._not_found_exception from e
        return result
