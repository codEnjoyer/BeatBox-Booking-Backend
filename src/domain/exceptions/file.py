from src.domain.exceptions.base import ItemNotFoundException, BadDataException


class FileNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "File"


class FileIsNotAnImageOrUnsupportedException(BadDataException):
    def __init__(self):
        super().__init__("File is not an image or has unsupported type")


class FileIsTooLargeException(BadDataException):
    def __init__(self):
        super().__init__("File is too large")
