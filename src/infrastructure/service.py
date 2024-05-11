from abc import ABC

from src.infrastructure.repository import Repository as RepositoryABC


class Service[Repository: RepositoryABC](ABC):
    _repository: Repository

    def __init__(self, repository: Repository):
        self._repository = repository
