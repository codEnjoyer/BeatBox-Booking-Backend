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
    orm_file, file_url = await file_service.create(file)

    return FileRead(
        name=str(orm_file.name), extension=str(orm_file.extension), url=file_url
    )


@router.get("/get/{name}", response_model=str)
async def get_file_url(file_service: FileServiceDep, name: str) -> str:
    return await file_service.get_url(name=name)


@router.delete("/delete/{name}")
async def delete(
    file_service: FileServiceDep, name: str, user: User = Depends(manager)
) -> str:
    await file_service.delete_by_name(name=name)
    return "Success delete"
