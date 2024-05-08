from src.infrastructure.item.operations import CreateOperation
from src.infrastructure.item.repository import Repository as RepositoryABC
from src.infrastructure.item.usecase import UseCase


class CreateItemUseCase[Item, Schema, Repository: RepositoryABC] \
            (UseCase[Repository], CreateOperation[Item, Schema]):

    async def create(self,
                     schema: Schema) -> Item:
        return await self._repository.create(schema)
