import uuid
from sqlalchemy import ColumnElement
from typing import Tuple
from fastapi import UploadFile
from filetype import guess

from src.domain.models import File
from src.domain.exceptions.studio import StudioNotFoundException
from src.domain.models.file import SupportedFileExtensions
from src.domain.schemas.file import FileUpdate, FileCreate, FileBucketRead
from src.domain.services.base import ModelService
from src.domain.models.repositories.file import FileRepository
from src.domain.models.repositories.file_bucket import FileBucketRepository


class FileService(ModelService[FileRepository, File, FileCreate, FileUpdate]):
    def __init__(self):
        super().__init__(FileRepository(), StudioNotFoundException)
        self.file_bucket_repository = FileBucketRepository()

    async def create(
        self, upload_file: UploadFile, **kwargs
    ) -> Tuple[File, FileBucketRead]:
        filename = str(uuid.uuid4())

        image_type = guess(upload_file.file)
        image_type_str = str(image_type.extension)
        full_name = f"{filename}.{image_type_str}"

        file_bucket_read: FileBucketRead = (
            await self.file_bucket_repository.upload(
                upload_file=upload_file, key=full_name
            )
        )
        file: File = await self._repository.create(
            FileCreate(
                name=filename, extension=SupportedFileExtensions(image_type_str)
            )
        )
        return file, file_bucket_read

    async def delete_by_name(self, name: str) -> None:
        file: File = await self._repository.get_one(self._model.name == name)
        full_name = f"{file.name}.{file.extension}"
        await self.file_bucket_repository.delete(file_key=full_name)
        return await self._repository.delete(self._model.name == name)

    async def get_url(self, name: uuid.UUID) -> FileBucketRead:
        file: File = await self._repository.get_one(self._model.name == name)
        full_name = f"{file.name}.{file.extension}"
        return await self.file_bucket_repository.get_presigned_url(full_name)

    async def update(
        self, schema: FileUpdate | dict[str, ...], *where: ColumnElement[bool]
    ) -> File:
        raise NotImplementedError('Method must not be called')
