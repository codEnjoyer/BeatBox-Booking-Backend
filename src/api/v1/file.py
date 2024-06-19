from fastapi import APIRouter
from starlette import status

from src.api.v1.dependencies.employee import StudioManagerDep
from src.api.v1.dependencies.file import (
    # ValidRoomImageFilenameDep,
    UploadImageFileDep,
    UploadImageFilesDep,
    StudioBannerFilenameDep,
    RoomBannerFilenameDep,
)
from src.api.v1.dependencies.room import ValidStudioRoomIdDep
from src.api.v1.dependencies.services import FileServiceDep, StudioServiceDep, \
    RoomServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep

router = APIRouter(tags=["File"])


@router.get(
    "/studios/{studio_id}/banner", tags=["Studio"]
)
async def get_studio_banner_url(
        banner_filename: StudioBannerFilenameDep,
        file_service: FileServiceDep,
) -> str:
    return await file_service.get_url_by_name(banner_filename)


@router.get(
    "/studios/{studio_id}/rooms/{room_id}/banner",
    tags=["Room"],
)
async def get_room_banner_url(
        banner_filename: RoomBannerFilenameDep,
        file_service: FileServiceDep,
) -> str:
    return await file_service.get_url_by_name(banner_filename)


@router.get(
    "/studios/{studio_id}/rooms/{room_id}/images",
    tags=["Room"],
)
async def get_room_images_urls(
        room: ValidStudioRoomIdDep,
        file_service: FileServiceDep,
) -> list[str]:
    urls = []
    for filename in room.images_filenames:
        urls.append(await file_service.get_url_by_name(filename))
    return urls


@router.post(
    "/studios/{studio_id}/rooms/{room_id}/images",
    tags=["Room"],
)
async def upload_room_images(
        room: ValidStudioRoomIdDep,
        image_files: UploadImageFilesDep,
        room_service: RoomServiceDep,
        file_service: FileServiceDep,
        _: StudioManagerDep,
) -> list[str]:
    filenames = []
    for image in image_files:
        filename = await file_service.upload_image(image)
        filenames.append(filename)
    new_filenames = room.images_filenames + filenames
    await room_service.update_by_id(room.id,
                                    {"images_filenames": new_filenames})
    urls = [await file_service.get_url_by_name(filename)
            for filename in filenames]
    return urls


@router.put(
    "/studios/{studio_id}/banner", tags=["Studio"],
)
async def update_studio_banner(
        studio: ValidStudioIdDep,
        image: UploadImageFileDep,
        file_service: FileServiceDep,
        studio_service: StudioServiceDep,
        _: StudioManagerDep,
) -> str:
    if studio.banner_filename is not None:
        await file_service.delete_by_name(studio.banner_filename)
    filename = await file_service.upload_image(image)
    await studio_service.update_by_id(studio.id, {"banner_filename": filename})
    return await file_service.get_url_by_name(filename)


@router.put(
    "/studios/{studio_id}/rooms/{room_id}/banner",
    tags=["Room"],
)
async def update_room_banner(
        room: ValidStudioRoomIdDep,
        file: UploadImageFileDep,
        room_service: RoomServiceDep,
        file_service: FileServiceDep,
        _: StudioManagerDep,
) -> str:
    if room.banner_filename is not None:
        await file_service.delete_by_name(room.banner_filename)
    filename = await file_service.upload_image(file)
    await room_service.update_by_id(room.id, {"banner_filename": filename})
    return await file_service.get_url_by_name(filename)


@router.delete(
    "/studios/{studio_id}/banner",
    tags=["Studio"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_studio_banner(
        studio: ValidStudioIdDep,
        banner: StudioBannerFilenameDep,
        studio_service: StudioServiceDep,
        file_service: FileServiceDep,
        _: StudioManagerDep,
):
    await studio_service.update_by_id(studio.id, {"banner_filename": None})
    await file_service.delete_by_name(banner)


@router.delete(
    "/studios/{studio_id}/rooms/{room_id}/banner",
    tags=["Room"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room_banner(
        room: ValidStudioRoomIdDep,
        banner: RoomBannerFilenameDep,
        room_service: RoomServiceDep,
        file_service: FileServiceDep,
        _: StudioManagerDep,
):
    await room_service.update_by_id(room.id, {"banner_filename": None})
    await file_service.delete_by_name(banner)


# @router.delete(
#     "/studios/{studio_id}/rooms/{room_id}/images/{filename}",
#     tags=["Room"],
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_room_image(
#         room: ValidStudioRoomIdDep,
#         image_filename: ValidRoomImageFilenameDep,
#         room_service: RoomServiceDep,
#         file_service: FileServiceDep,
#         _: StudioManagerDep,
# ):
#     new_room_filenames = [filename for filename in room.images_filenames
#                           if filename != image_filename]
#     await room_service.update_by_id(room.id,
#                                     {"images_filenames": new_room_filenames})
#     await file_service.delete_by_name(image_filename)
