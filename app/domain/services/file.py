import uuid

from fastapi import UploadFile
from filetype import guess
from filetype.types import image

from app.domain.exceptions.file import (
    FileIsNotAnImageOrUnsupportedException,
    FileIsTooLargeException,
)
from app.domain.models.repositories.s3 import S3Repository

MAX_IMAGE_SIZE = 1024 * 1024 * 10  # 10 Mb
VALID_IMAGE_EXTENSIONS = (
    image.Jpeg().extension,
    image.Png().extension,
    image.Webp().extension,
)


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
