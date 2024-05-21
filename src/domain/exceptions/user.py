from src.domain.exceptions.base import BBBException


class UserAlreadyExistsException(BBBException):
    pass


class UserNotFoundException(BBBException):
    pass
