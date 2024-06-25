from app.domain.exceptions.base import ItemNotFoundException, BadDataException


class ReviewNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Review"


class ReviewAlreadyExistException(BadDataException):
    def __init__(self):
        super().__init__("Review already exists")
