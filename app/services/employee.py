from exceptions.employee import EmployeeNotFoundException
from models import Employee
from models.repositories.employee import EmployeeRepository
from schemas.employee import EmployeeCreate, EmployeeUpdate
from services.base import ModelService


class EmployeeService(
    ModelService[EmployeeRepository, Employee, EmployeeCreate, EmployeeUpdate]
):
    def __init__(self):
        super().__init__(EmployeeRepository(), EmployeeNotFoundException)

    async def get_all_by_studio_id(
        self, studio_id: int, offset: int = 0, limit: int = 100
    ) -> list[Employee]:
        return await self._repository.get_all(
            Employee.studio_id == studio_id, limit=limit, offset=offset
        )

    async def add_in_studio(
        self, studio_id: int, schema: EmployeeCreate
    ) -> Employee:
        schema_dict = schema.model_dump()
        schema_dict["studio_id"] = studio_id
        return await self._repository.create(schema_dict)
