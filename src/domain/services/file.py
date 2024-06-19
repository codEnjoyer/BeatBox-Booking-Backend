import uuid
from dataclasses import dataclass

from fastapi import UploadFile
from filetype import guess
from filetype.types import image

from src.domain.exceptions.file import (
    FileIsNotAnImageOrUnsupportedException,
    FileIsTooLargeException,
)
from src.domain.models.repositories.s3 import S3Repository

MAX_IMAGE_SIZE = 1024 * 1024 * 10  # 10 Mb
VALID_IMAGE_EXTENSIONS = (
    image.Jpeg().extension,
    image.Png().extension,
    image.Webp().extension,
)


@dataclass
class File:
    url: str
    extension: str


class FileService:
    def __init__(self):
        self._repository = S3Repository()

    async def upload_image(self, upload_file: UploadFile) -> str:
        image_extension = guess(upload_file.file).extension
        filename = f"{uuid.uuid4()}.{image_extension}"
        await self._repository.upload(upload_file, filename)
        return filename

    async def get_url_by_name(self, filename: str) -> str:
        return await self._repository.get_url(filename)

    async def delete_by_name(self, filename: str) -> None:
        await self._repository.delete(filename)

    # async def delete_by_name(self, name: str) -> None:
    #     try:
    #         file: File =
    #         await self._repository.get_one(self.model.name == name)
    #         full_name = f"{file.name}.{file.extension.value}"
    #         await self.file_bucket_repository.delete(file_key=full_name)
    #         await self._repository.delete(self.model.name == name)
    #     except Exception:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
    #         )

    @staticmethod
    def check_if_file_valid_image(upload_file: UploadFile) -> None:
        if upload_file.size > MAX_IMAGE_SIZE:
            raise FileIsTooLargeException()
        file_type = guess(upload_file.file)
        if (
            file_type is None
            or file_type.extension not in VALID_IMAGE_EXTENSIONS
        ):
            raise FileIsNotAnImageOrUnsupportedException()
