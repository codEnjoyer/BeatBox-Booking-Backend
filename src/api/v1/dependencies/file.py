import uuid
from typing import Annotated

from fastapi import UploadFile, HTTPException, Depends
from starlette import status

from src.api.v1.dependencies.room import ValidStudioRoomIdDep
from src.api.v1.dependencies.services import FileServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep


async def valid_filename(filename: uuid.UUID,
                         file_service: FileServiceDep) -> uuid.UUID:
    ...


ValidFilenameDep = Annotated[uuid.UUID, Depends(valid_filename)]


async def valid_room_image_filename(room: ValidStudioRoomIdDep,
                                    filename: ValidFilenameDep) -> uuid.UUID:
    ...


ValidRoomImageFilenameDep = Annotated[
    uuid.UUID, Depends(valid_room_image_filename)]


async def existing_studio_banner(studio: ValidStudioIdDep) -> uuid.UUID:
    if studio.banner_filename is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Studio has no banner"
        )
    return studio.banner_filename


StudioBannerDep = Annotated[uuid.UUID, Depends(existing_studio_banner)]


async def existing_room_banner(room: ValidStudioRoomIdDep) -> uuid.UUID:
    if room.banner_filename is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room has no banner"
        )
    return room.banner_filename


RoomBannerDep = Annotated[uuid.UUID, Depends(existing_room_banner)]


async def valid_upload_image_file(file: UploadFile) -> UploadFile:
    # if not file.content_type.startswith("image"):
    #     raise HTTPException(
    #         status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    #         detail="File must be an image"
    #     )
    # TODO
    return file


UploadImageFileDep = Annotated[UploadFile, Depends(valid_upload_image_file)]


async def valid_upload_image_files(files: list[UploadFile]) -> list[UploadFile]:
    return files


UploadImageFilesDep = Annotated[
    list[UploadFile], Depends(valid_upload_image_files)]
