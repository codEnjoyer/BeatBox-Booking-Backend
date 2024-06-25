from typing import override

from app.domain.models import Employee
from app.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from app.domain.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(
    SQLAlchemyRepository[Employee, EmployeeCreate, EmployeeUpdate]
):
    @override
    @property
    def model(self) -> type[Employee]:
        return Employee
