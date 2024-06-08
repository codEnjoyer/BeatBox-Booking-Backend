from typing import Annotated

from fastapi import Depends

from src.domain.services.file import FileService


def get_file_service() -> FileService:
    return FileService()


FileServiceDep = Annotated[FileService, Depends(get_file_service)]
