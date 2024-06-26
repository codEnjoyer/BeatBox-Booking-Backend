from fastapi import APIRouter, HTTPException
from starlette import status

from api.v1.dependencies.employee import (
    ValidEmployeeIdDep,
    StudioManagerDep,
)
from api.v1.dependencies.services import EmployeeServiceDep, UserServiceDep
from api.v1.dependencies.studio import ValidStudioIdDep
from api.v1.dependencies.types import QueryOffset, QueryLimit
from exceptions.user import UserNotFoundException
from models import Employee
from schemas.employee import EmployeeRead, EmployeeCreate

router = APIRouter(tags=["Employee"])


@router.get(
    "/studios/{studio_id}/employees",
    tags=["Employee"],
    response_model=list[EmployeeRead],
)
async def get_studio_employees(
    studio: ValidStudioIdDep,
    employee_service: EmployeeServiceDep,
    _: StudioManagerDep,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[Employee]:
    return await employee_service.get_all_by_studio_id(
        studio.id, offset=offset, limit=limit
    )


@router.post("/studios/{studio_id}/employees", response_model=EmployeeRead)
async def create_employee_in_studio(
    studio: ValidStudioIdDep,
    schema: EmployeeCreate,
    employee_service: EmployeeServiceDep,
    user_service: UserServiceDep,
    _: StudioManagerDep,
) -> Employee:
    try:
        user = await user_service.get_by_id(schema.user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    if user.employee is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already is an employee",
        )
    return await employee_service.add_in_studio(studio.id, schema)


@router.delete(
    "/studios/{studio_id}/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
    employee: ValidEmployeeIdDep,
    employee_service: EmployeeServiceDep,
    _: StudioManagerDep,
) -> None:
    await employee_service.delete_by_id(employee.id)
