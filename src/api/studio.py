from fastapi import APIRouter, Depends

from src.api.dependencies.services.studio import StudioServiceDep
from src.domain.models import Studio
from src.domain.schemas.studio import StudioRead, StudioCreate, StudioUpdate
from src.api.dependencies.auth import manager
from src.domain.models.user import User
from src.api.dependencies.studio import convert_model_to_scheme

router = APIRouter(prefix="/studios", tags=["Studio"])


@router.get("", response_model=list[StudioRead])
async def get_all_studios(
    studio_service: StudioServiceDep, offset: int = 0, limit: int = 100
) -> list[Studio]:
    return await studio_service.get_all(offset=offset, limit=limit)


@router.post("/create", response_model=StudioRead)
async def create_studio(
    schema: StudioCreate, studio_service: StudioServiceDep
) -> StudioRead:
    studio = await studio_service.create(schema=schema)
    return convert_model_to_scheme(studio)


@router.patch("{studio_id}/update", response_model=StudioRead)
async def update_studio(
    studio_id: int,
    schema: StudioUpdate,
    studio_service: StudioServiceDep,
    user: User = Depends(manager),
) -> StudioRead:
    studio = await studio_service.update(
        studio_id=studio_id, user_id=user.id, schema=schema
    )
    return convert_model_to_scheme(studio)


@router.delete("{studio_id}/delete")
async def delete_studio(
    studio_id: int,
    studio_service: StudioServiceDep,
    user: User = Depends(manager),
) -> str:
    await studio_service.delete(studio_id=studio_id, user_id=user.id)
    return "Success delete studio"
