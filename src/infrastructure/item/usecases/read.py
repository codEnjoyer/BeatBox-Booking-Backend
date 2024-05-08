from src.infrastructure.exceptions import ItemNotFoundException
from src.infrastructure.item.operations import GetOneOperation, GetAllOperation
from src.infrastructure.item.repository import Repository as RepositoryABC
from src.infrastructure.item.usecase import UseCase


class GetOneItemUseCase[Item, Repository: RepositoryABC] \
            (UseCase[Repository], GetOneOperation[Item]):
    _not_found_exception: Exception

    async def get_one(self,
                      *where) -> Item:
        try:
            result = await self._repository.get_one(*where)
        except ItemNotFoundException as e:
            raise self._not_found_exception from e
        return result


class GetAllItemsUseCase[Item, Repository: RepositoryABC] \
            (UseCase[Repository], GetAllOperation[Item]):
    async def get_all(self,
                      *where,
                      offset: int = 0,
                      limit: int = 100) -> list[Item]:
        return await self._repository.get_all(*where,
                                              offset=offset,
                                              limit=limit)
