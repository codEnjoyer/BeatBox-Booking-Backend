from typing import override

from models import Employee
from models.repositories.SQLAlchemy import SQLAlchemyRepository
from schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(
    SQLAlchemyRepository[Employee, EmployeeCreate, EmployeeUpdate]
):
    @override
    @property
    def model(self) -> type[Employee]:
        return Employee
