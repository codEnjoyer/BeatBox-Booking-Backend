from abc import ABC, abstractmethod

from src.infrastructure.item.operations.base import RepositoryOperation


class GetOperation[Item](RepositoryOperation, ABC):
    @abstractmethod
    async def get_all(self,
                      *where,
                      offset: int = 0,
                      limit: int = 100) -> list[Item]:
        ...

    @abstractmethod
    async def get_one(self,
                      *where) -> Item | None:
        ...
