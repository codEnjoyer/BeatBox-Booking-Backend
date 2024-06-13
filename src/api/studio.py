from fastapi import APIRouter, Depends

from src.api.dependencies.services import EmployeeServiceDep
from src.api.dependencies.services import StudioServiceDep
from src.api.dependencies.studio import ValidStudioIdDep
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
async def get_studio(studio: ValidStudioIdDep) -> StudioRead:
    return studio


@router.post(
    "", dependencies=[Depends(get_current_superuser)], response_model=StudioRead
)
async def create_studio(
    schema: StudioCreate,
    studio_service: StudioServiceDep,
) -> StudioRead:
    studio = await studio_service.create(schema=schema)
    return studio


@router.put("/{studio_id}", response_model=StudioRead)
async def update_studio(
    schema: StudioUpdate,
    studio: ValidStudioIdDep,
    studio_service: StudioServiceDep,
    _: AuthenticatedEmployee,
) -> StudioRead:
    studio = await studio_service.update(studio.id, schema)
    return studio


@router.delete("/{studio_id}")
async def delete_studio(
    studio: ValidStudioIdDep,
    studio_service: StudioServiceDep,
    employee: AuthenticatedEmployee,
) -> None:
    await studio_service.delete(studio.id, employee.user_id)


@router.get(
    "/{studio_id}/employees",
    tags=["Employee"],
    dependencies=[Depends(get_current_user_employee)],
    response_model=list[EmployeeRead],
)
async def get_all_studio_employees(
    studio: ValidStudioIdDep,
    employee_service: EmployeeServiceDep,
    limit: int = 100,
    offset: int = 0,
) -> list[Employee]:
    return await employee_service.get_all_by_studio_id(
        studio.id, limit=limit, offset=offset
    )
