from fastapi import APIRouter, Depends

from src.api.dependencies.services import EmployeeServiceDep
from src.api.dependencies.services import StudioServiceDep
from src.api.dependencies.studio import ValidStudioIdDep, StudioEmployeeDep
from src.domain.models import Employee
from src.domain.schemas.employee import EmployeeRead
from src.domain.schemas.studio import StudioRead, StudioCreate, StudioUpdate
from src.api.dependencies.auth import get_current_superuser

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
    studio_service: StudioServiceDep,
    studio_employee: StudioEmployeeDep,
) -> StudioRead:
    studio = await studio_service.update_by_id(
        studio_employee.studio_id, schema
    )
    return studio


@router.delete(
    "/{studio_id}",
    dependencies=[Depends(get_current_superuser)],
)
async def delete_studio(
    studio: ValidStudioIdDep,
    studio_service: StudioServiceDep,
) -> None:
    await studio_service.delete_by_id(studio.id)


@router.get(
    "/{studio_id}/employees",
    tags=["Employee"],
    response_model=list[EmployeeRead],
)
async def get_all_studio_employees(
    studio: ValidStudioIdDep,
    _: StudioEmployeeDep,
    employee_service: EmployeeServiceDep,
    limit: int = 100,
    offset: int = 0,
) -> list[Employee]:
    return await employee_service.get_all_by_studio_id(
        studio.id, limit=limit, offset=offset
    )
