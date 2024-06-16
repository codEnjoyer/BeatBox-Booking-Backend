from src.domain.exceptions.base import ItemNotFoundException


class FileNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "File"
