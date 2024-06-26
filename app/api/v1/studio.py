from fastapi import APIRouter
from starlette import status

from api.v1.dependencies.auth import AuthenticatedSuperuser
from api.v1.dependencies.employee import StudioManagerDep
from api.v1.dependencies.services import StudioServiceDep
from api.v1.dependencies.studio import ValidStudioIdDep
from api.v1.dependencies.types import QueryOffset, QueryLimit
from schemas.studio import StudioRead, StudioCreate, StudioUpdate

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


@router.post("", response_model=StudioRead)
async def create_studio(
    schema: StudioCreate,
    studio_service: StudioServiceDep,
    _: AuthenticatedSuperuser,
) -> StudioRead:
    return await studio_service.create(schema)


@router.put("/{studio_id}", response_model=StudioRead)
async def update_studio(
    studio: ValidStudioIdDep,
    schema: StudioUpdate,
    studio_service: StudioServiceDep,
    _: StudioManagerDep,
) -> StudioRead:
    return await studio_service.update_by_id(studio.id, schema)


@router.delete(
    "/{studio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_studio(
    studio: ValidStudioIdDep,
    studio_service: StudioServiceDep,
    _: AuthenticatedSuperuser,
) -> None:
    await studio_service.delete_by_id(studio.id)
