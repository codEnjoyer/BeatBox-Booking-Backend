from fastapi import APIRouter, Depends

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.services import FileServiceDep
from src.domain.schemas.file import FileRead
from fastapi import UploadFile

router = APIRouter(prefix="/files", tags=["File"])


@router.post(
    "",
    dependencies=[Depends(get_current_user)],
    response_model=FileRead,
)
async def upload_file(
    file: UploadFile, file_service: FileServiceDep
) -> FileRead:
    orm_file, file_url = await file_service.create(file)

    return FileRead(
        name=str(orm_file.name), extension=str(orm_file.extension), url=file_url
    )
    # TODO: перенести в создание студии и комнаты


@router.get(
    "/{name}", dependencies=[Depends(get_current_user)], response_model=FileRead
)
async def get_file_url(name: str, file_service: FileServiceDep) -> str:
    return await file_service.get_url(name=name)


@router.delete("/{name}", dependencies=[Depends(get_current_user)])
async def delete(name: str, file_service: FileServiceDep) -> None:
    await file_service.delete_by_name(name=name)
