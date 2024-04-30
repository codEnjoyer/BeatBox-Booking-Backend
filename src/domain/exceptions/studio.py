from src.domain.exceptions.base import BBBException
from src.infrastructure.exceptions import ItemNotFoundException


class StudioNotFoundException(BBBException, ItemNotFoundException):
    ...
