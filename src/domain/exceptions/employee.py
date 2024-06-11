from sqlalchemy.exc import NoResultFound

from src.domain.exceptions.base import BBBException


class EmployeeNotFoundException(BBBException, NoResultFound):
    ...
