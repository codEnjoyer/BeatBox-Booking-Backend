from abc import ABC


class RepositoryOperation[Item](ABC):
    _model: type[Item]

    def __init__(self, model: type[Item]):
        self._model = model
