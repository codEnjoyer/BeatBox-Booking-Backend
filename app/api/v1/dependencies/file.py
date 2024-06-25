from typing import Annotated

from fastapi import UploadFile, HTTPException, Depends
from starlette import status

from app.api.v1.dependencies.room import ValidStudioRoomIdDep
from app.api.v1.dependencies.services import FileServiceDep
from app.api.v1.dependencies.studio import ValidStudioIdDep
from app.domain.exceptions.file import (
    FileNotFoundException,
    FileIsTooLargeException,
    FileIsNotAnImageOrUnsupportedException,
)


async def valid_filename(filename: str, file_service: FileServiceDep) -> str:
    try:
        await file_service.get_url_by_name(filename)
    except FileNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    return filename


ValidFilenameDep = Annotated[str, Depends(valid_filename)]


async def valid_room_image_filename(
    room: ValidStudioRoomIdDep, filename: ValidFilenameDep
) -> str:
    if not room.has_image_with_filename(filename):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    return filename


ValidRoomImageFilenameDep = Annotated[str, Depends(valid_room_image_filename)]


async def existing_studio_banner(studio: ValidStudioIdDep) -> str:
    if studio.banner_filename is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Studio has no banner"
        )
    return studio.banner_filename


StudioBannerFilenameDep = Annotated[str, Depends(existing_studio_banner)]


async def existing_room_banner(room: ValidStudioRoomIdDep) -> str:
    if room.banner_filename is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room has no banner"
        )
    return room.banner_filename


RoomBannerFilenameDep = Annotated[str, Depends(existing_room_banner)]


async def valid_upload_image_file(
    file: UploadFile, file_service: FileServiceDep
) -> UploadFile:
    try:
        file_service.check_if_file_valid_image(file)
    except FileIsNotAnImageOrUnsupportedException as e:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(e)
        )
    except FileIsTooLargeException as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(e)
        )
    return file


UploadImageFileDep = Annotated[UploadFile, Depends(valid_upload_image_file)]


async def valid_upload_image_files(
    files: list[UploadFile], file_service: FileServiceDep
) -> list[UploadFile]:
    try:
        for file in files:
            file_service.check_if_file_valid_image(file)
    except FileIsNotAnImageOrUnsupportedException as e:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(e)
        )
    except FileIsTooLargeException as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(e)
        )
    return files


UploadImageFilesDep = Annotated[
    list[UploadFile], Depends(valid_upload_image_files)
]
