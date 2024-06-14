from enum import StrEnum

# from sqlalchemy import ColumnElement
# from typing import Tuple
# from fastapi import UploadFile, HTTPException
# from filetype import guess
# from starlette import status
#
# from src.domain.exceptions.studio import StudioNotFoundException
# from src.domain.services.base import ModelService
# from src.domain.models.repositories.file import FileRepository
# from src.domain.models.repositories.file_bucket import FileBucketRepository


class SupportedImageFileExtensions(StrEnum):
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"
    JPG = "jpg"


class FileService: ...


# class FileService(ModelService[FileRepository, File, FileCreate, FileUpdate]):
#     def __init__(self):
#         super().__init__(FileRepository(), StudioNotFoundException)
#         self.file_bucket_repository = FileBucketRepository()
#
#     async def create(
#             self, upload_file: UploadFile, **kwargs
#     ) -> Tuple[File, str]:
#         filename = str(uuid.uuid4())
#
#         image_type = guess(upload_file.file)
#         image_type_str = str(image_type.extension)
#         full_name = f"{filename}.{image_type_str}"
#
#         file_url = await self.file_bucket_repository.upload(
#             upload_file=upload_file, key=full_name
#         )
#         file: File = await self._repository.create(
#             FileCreate(
#                 name=filename,
#                 extension=SupportedFileExtensions(image_type_str)
#             )
#         )
#         return file, file_url
#
#     async def delete_by_name(self, name: str) -> None:
#         try:
#             file: File =
#               await self._repository.get_one(self.model.name == name)
#             full_name = f"{file.name}.{file.extension.value}"
#             await self.file_bucket_repository.delete(file_key=full_name)
#             await self._repository.delete(self.model.name == name)
#         except Exception:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
#             )
#
#     async def get_url(self, name: str) -> str:
#         try:
#             file: File =
#               await self._repository.get_one(self.model.name == name)
#             full_name = f"{file.name}.{file.extension.value}"
#             return await self.file_bucket_repository.get_presigned_url(
#                 full_name
#             )
#         except Exception:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
#             )
#
#     async def try_get_url(self, name: str) -> str | None:
#         try:
#             file: File =
#               await self._repository.get_one(self.model.name == name)
#             full_name = f"{file.name}.{file.extension.value}"
#             return await self.file_bucket_repository.get_presigned_url(
#                 full_name
#             )
#         except Exception:
#             return None
#
#     async def update(
#             self, schema: FileUpdate | dict[str, ...],
#             *where: ColumnElement[bool]
#     ) -> File:
#         raise NotImplementedError('Method must not be called')
