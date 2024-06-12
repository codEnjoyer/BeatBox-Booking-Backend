from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.api.dependencies.services import FileServiceDep
from src.api.dependencies.services import RoomServiceDep
from src.domain.schemas.room import RoomRead, RoomCreate, RoomUpdate
from src.api.dependencies.auth import AuthenticatedEmployee
from src.api.dependencies.room import convert_model_to_scheme, get_images_url

router = APIRouter(tags=["Room"])


@router.get("/studios/{studio_id}/rooms/{room_id}", response_model=RoomRead)
async def get_room(
    studio_id: int,  # noqa
    room_id: int,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
) -> RoomRead:
    try:
        room = await room_service.get(room_id)
        banner_url, images_url = await get_images_url(
            room=room, file_service=file_service, room_service=room_service
        )
        return convert_model_to_scheme(
            room=room, banner_url=banner_url, images_url=images_url
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )


# @router.get("/all/{studio_id}", response_model=list[RoomRead])
# async def get_all_studio_rooms(
#         studio_id: int,
#         room_service: RoomServiceDep,
#         file_service: FileServiceDep,
# ) -> list[RoomRead]:
#     try:
#         rooms = await room_service.get_all(Room.studio_id == studio_id)
#         banner_and_images = [
#             await get_images_url(room=room,
#                                  file_service=file_service,
#                                  room_service=room_service
#             )
#             for room in rooms
#         ]
#
#         return [
#             convert_model_to_scheme(
#                 room=rooms[i],
#                 banner_url=banner_and_images[i][0],
#                 images_url=banner_and_images[i][1],
#             )
#             for i in range(len(rooms))
#         ]
#
#     except NoResultFound:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
#         )


@router.post("/studios/{studio_id}/rooms", response_model=RoomRead)
async def create_room_in_studio(
    studio_id: int,
    schema: RoomCreate,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    employee: AuthenticatedEmployee,
) -> RoomRead:
    room = await room_service.create(
        schema=schema, studio_id=studio_id, employee_id=employee.id
    )
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )


@router.put("/studios/{studio_id}/rooms/{room_id}", response_model=RoomRead)
async def update_room(
    studio_id: int,
    room_id: int,
    schema: RoomUpdate,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    employee: AuthenticatedEmployee,
) -> RoomRead:
    room = await room_service.update(room_id, studio_id, employee.id, schema)
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )


@router.delete("/studios/{studio_id}/rooms/{room_id}")
async def delete_room(
    studio_id: int,
    room_id: int,
    room_service: RoomServiceDep,
    employee: AuthenticatedEmployee,
) -> None:
    await room_service.delete(room_id, studio_id, employee.id)
