from src.domain.models import Employee
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(
    SQLAlchemyRepository[Employee, EmployeeCreate, EmployeeUpdate]
):
    def __init__(self):
        super().__init__(Employee)
