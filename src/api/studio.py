from fastapi import APIRouter, Depends

from src.api.dependencies.services import EmployeeServiceDep
from src.api.dependencies.services import StudioServiceDep
from src.domain.models import Employee
from src.domain.schemas.employee import EmployeeRead
from src.domain.schemas.studio import StudioRead, StudioCreate, StudioUpdate
from src.api.dependencies.auth import (
    AuthenticatedEmployee,
    get_current_superuser,
    get_current_user_employee,
)

router = APIRouter(prefix="/studios", tags=["Studio"])


@router.get("", response_model=list[StudioRead])
async def get_all_studios(
    studio_service: StudioServiceDep, offset: int = 0, limit: int = 100
) -> list[StudioRead]:
    studios = await studio_service.get_all(offset=offset, limit=limit)
    return studios


@router.get("/{studio_id}", response_model=StudioRead)
async def get_studio(
    studio_id: int, studio_service: StudioServiceDep
) -> StudioRead:
    studio = await studio_service.get_by_id(model_id=studio_id)
    return studio


@router.post(
    "/create",
    dependencies=[Depends(get_current_superuser)],
    response_model=StudioRead,
)
async def create_studio(
    schema: StudioCreate,
    studio_service: StudioServiceDep,
) -> StudioRead:
    studio = await studio_service.create(schema=schema)
    return studio


@router.patch("/{studio_id}/update", response_model=StudioRead)
async def update_studio(
    studio_id: int,
    schema: StudioUpdate,
    studio_service: StudioServiceDep,
    employee: AuthenticatedEmployee,
) -> StudioRead:
    studio = await studio_service.update(
        studio_id=studio_id, user_id=employee.user_id, schema=schema
    )
    return studio


@router.delete("/{studio_id}/delete")
async def delete_studio(
    studio_id: int,
    studio_service: StudioServiceDep,
    employee: AuthenticatedEmployee,
) -> str:
    await studio_service.delete(studio_id=studio_id, user_id=employee.user_id)
    return "Success delete studio"


@router.get(
    "/{studio_id}/employees",
    tags=["Employee"],
    dependencies=[Depends(get_current_user_employee)],
    response_model=list[EmployeeRead],
)
async def get_all_studio_employees(
    studio_id: int,
    employee_service: EmployeeServiceDep,
    limit: int = 100,
    offset: int = 0,
) -> list[Employee]:
    return await employee_service.get_all_by_studio_id(
        studio_id, limit=limit, offset=offset
    )
