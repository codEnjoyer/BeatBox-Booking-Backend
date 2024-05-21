from fastapi import APIRouter, Depends

from src.api.dependencies.auth import (
    get_current_superuser,
    get_current_user_employee,
)
from src.api.dependencies.employee import can_create_employee
from src.api.dependencies.services.employee import EmployeeServiceDep
from src.domain.models import Employee
from src.domain.schemas.employee import EmployeeRead, EmployeeCreate

router = APIRouter(prefix="/employees", tags=["Employee"])


@router.get(
    "",
    dependencies=[Depends(get_current_superuser)],
    response_model=list[EmployeeRead],
)
async def get_all_employees(
    employee_service: EmployeeServiceDep, limit: int = 100, offset: int = 0
) -> list[Employee]:
    return await employee_service.get_all(limit=limit, offset=offset)


@router.post(
    "", dependencies=[Depends(can_create_employee)], response_model=EmployeeRead
)
async def create_studio_employee(
    schema: EmployeeCreate, employee_service: EmployeeServiceDep
) -> Employee:
    return await employee_service.create(schema)


@router.delete(
    "/{employee_id}", dependencies=[Depends(get_current_user_employee)]
)
async def delete_employee(
    employee_id: int, employee_service: EmployeeServiceDep
) -> None:
    return await employee_service.delete_by_id(employee_id)
