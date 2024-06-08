from typing import Annotated

from fastapi import Depends

from src.domain.services.employee import EmployeeService


def get_employee_service() -> EmployeeService:
    return EmployeeService()


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]
