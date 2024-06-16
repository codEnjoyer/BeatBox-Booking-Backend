from src.domain.exceptions.base import ItemNotFoundException


class StudioNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Studio"
