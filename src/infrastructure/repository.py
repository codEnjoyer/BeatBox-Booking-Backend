from abc import ABC, abstractmethod


class Repository[Item, CreateSchema, UpdateSchema](ABC):

    @abstractmethod
    async def create(self, schema: CreateSchema) -> Item: ...

    @abstractmethod
    async def get_all(
        self, *where, options=None, offset: int = 0, limit: int = 100
    ) -> list[Item]: ...

    @abstractmethod
    async def get_one(self, *where, options=None) -> Item: ...

    @abstractmethod
    async def update(
        self, schema: UpdateSchema, *where
    ) -> Item | list[Item]: ...

    @abstractmethod
    async def delete(self, *where) -> None: ...
