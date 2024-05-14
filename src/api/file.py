from fastapi import APIRouter, Depends

from src.api.dependencies.auth import manager
from src.api.dependencies.services.file import FileServiceDep
from src.domain.models import User
from src.domain.schemas.file import FileRead
from fastapi import UploadFile

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload", response_model=FileRead)
async def upload_file(
    file_service: FileServiceDep,
    file: UploadFile,
    user: User = Depends(manager),
) -> FileRead:
    file = await file_service.create(file)
    return FileRead(
        name=file[0].name, extension=file[0].extension, url=file[1].url
    )


@router.get("/get", response_model=FileRead)
async def get_file_url(file_service: FileServiceDep, name: str) -> str:
    return await file_service.get_url(name=name)


@router.delete("/delete")
async def delete(file_service: FileServiceDep, name: str) -> str:
    return await file_service.delete_by_name(name=name)
