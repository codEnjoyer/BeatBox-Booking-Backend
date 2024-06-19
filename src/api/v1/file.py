from fastapi import APIRouter
from starlette import status

from src.api.v1.dependencies.employee import StudioManagerDep
from src.api.v1.dependencies.file import ValidRoomImageFilenameDep, \
    UploadImageFileDep, UploadImageFilesDep, StudioBannerDep, RoomBannerDep
from src.api.v1.dependencies.room import ValidStudioRoomIdDep
from src.api.v1.dependencies.services import FileServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep
from src.domain.schemas.file import FileRead

router = APIRouter(tags=["File"])


@router.get("/studios/{studio_id}/banner",
            tags=["Studio"],
            response_model=FileRead)
async def get_studio_banner_url(
        banner: StudioBannerDep,
):
    ...


@router.get("/studios/{studio_id}/rooms/{room_id}/banner",
            tags=["Room"],
            response_model=FileRead)
async def get_room_banner_url(
        banner: RoomBannerDep,
):
    ...


@router.get("/studios/{studio_id}/rooms/{room_id}/images",
            tags=["Room"],
            response_model=list[FileRead])
async def get_room_images_urls(
        room: ValidStudioRoomIdDep,
):
    ...


@router.post("/studios/{studio_id}/rooms/{room_id}/images",
             tags=["Room"],
             response_model=list[FileRead])
async def upload_room_images(
        room: ValidStudioRoomIdDep,
        image_files: UploadImageFilesDep,
        file_service: FileServiceDep,
        _: StudioManagerDep
):
    ...


@router.put("/studios/{studio_id}/banner",
            tags=["Studio"],
            response_model=FileRead)
async def update_studio_banner(
        studio: ValidStudioIdDep,
        file: UploadImageFileDep,
        file_service: FileServiceDep,
        _: StudioManagerDep
):
    ...


@router.put("/studios/{studio_id}/rooms/{room_id}/banner",
            tags=["Room"],
            response_model=FileRead)
async def update_room_banner(
        room: ValidStudioRoomIdDep,
        file: UploadImageFileDep,
        file_service: FileServiceDep,
        _: StudioManagerDep
):
    ...


@router.delete("/studios/{studio_id}/banner",
               tags=["Studio"],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_studio_banner(
        studio: ValidStudioIdDep,
        banner: StudioBannerDep,
        file_service: FileServiceDep,
        _: StudioManagerDep
):
    ...


@router.delete("/studios/{studio_id}/rooms/{room_id}/banner",
               tags=["Room"],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_banner(
        room: ValidStudioRoomIdDep,
        banner: RoomBannerDep,
        file_service: FileServiceDep,
        _: StudioManagerDep
):
    ...


@router.delete("/studios/{studio_id}/rooms/{room_id}/images/{filename}",
               tags=["Room"],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_image(
        room: ValidStudioRoomIdDep,
        image_filename: ValidRoomImageFilenameDep,
        file_service: FileServiceDep,
        _: StudioManagerDep
):
    ...
