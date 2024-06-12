from src.domain.exceptions.base import ItemNotFoundException


class ReviewNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Review"
