from fastapi import APIRouter

from src.api.dependencies.employee import ValidEmployeeIdDep, StudioManagerDep
from src.api.dependencies.services import EmployeeServiceDep
from src.api.dependencies.studio import ValidStudioIdDep
from src.api.dependencies.types import QueryOffset, QueryLimit
from src.domain.models import Employee
from src.domain.schemas.employee import EmployeeRead, EmployeeCreate

router = APIRouter(tags=["Employee"])


@router.get(
    "/studios/{studio_id}/employees",
    tags=["Employee"],
    response_model=list[EmployeeRead],
)
async def get_studio_employees(
    studio: ValidStudioIdDep,
    _: StudioManagerDep,
    employee_service: EmployeeServiceDep,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[Employee]:
    return await employee_service.get_all_by_studio_id(
        studio.id, offset=offset, limit=limit
    )


@router.post("/studios/{studio_id}/employees", response_model=EmployeeRead)
async def create_employee_in_studio(
    schema: EmployeeCreate,
    _: StudioManagerDep,
    employee_service: EmployeeServiceDep,
) -> Employee:
    return await employee_service.create(schema)


@router.delete(
    "/studios/{studio_id}/employees/{employee_id}",
)
async def delete_employee(
    _: StudioManagerDep,
    employee: ValidEmployeeIdDep,
    employee_service: EmployeeServiceDep,
) -> None:
    await employee_service.delete_by_id(employee.id)
