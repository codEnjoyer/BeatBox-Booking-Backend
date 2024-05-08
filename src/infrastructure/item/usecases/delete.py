from src.infrastructure.exceptions import ItemNotFoundException
from src.infrastructure.item.repository import Repository as RepositoryABC
from src.infrastructure.item.usecase import UseCase


class DeleteItemUseCase[Repository: RepositoryABC] \
            (UseCase[Repository]):
    _not_found_exception: Exception

    async def delete(self,
                     *where) -> None:
        try:
            await self._repository.delete(*where)
        except ItemNotFoundException as e:
            raise self._not_found_exception from e
