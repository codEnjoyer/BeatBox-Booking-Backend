from fastapi import APIRouter, Depends

from src.api.v1.dependencies.services import StudioServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep, StudioEmployeeDep
from src.api.v1.dependencies.types import QueryOffset, QueryLimit
from src.api.v1.dependencies.auth import get_current_superuser
from src.domain.schemas.studio import StudioRead, StudioCreate, StudioUpdate

router = APIRouter(prefix="/studios", tags=["Studio"])


@router.get("", response_model=list[StudioRead])
async def get_all_studios(
    studio_service: StudioServiceDep,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
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
