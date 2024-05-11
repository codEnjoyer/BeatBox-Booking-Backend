from fastapi import APIRouter

from src.api.dependencies.services.studio import StudioServiceDep
from src.domain.models import Studio
from src.domain.schemas.studio import StudioRead

router = APIRouter(prefix="/studios", tags=["Studio"])


@router.get("", response_model=list[StudioRead])
async def get_all_studios(studio_service: StudioServiceDep,
                          offset: int = 0,
                          limit: int = 100) -> list[Studio]:
    return await studio_service.get_all(offset=offset, limit=limit)
