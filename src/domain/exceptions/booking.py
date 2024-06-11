from sqlalchemy.exc import NoResultFound

from src.domain.exceptions.base import BBBException


class BookingNotFoundException(BBBException, NoResultFound):
    ...
