from typing import override

from src.domain.models import Employee
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(
    SQLAlchemyRepository[Employee, EmployeeCreate, EmployeeUpdate]
):
    @override
    @property
    def model(self) -> type[Employee]:
        return Employee
