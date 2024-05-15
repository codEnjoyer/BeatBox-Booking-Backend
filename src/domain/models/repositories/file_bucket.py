from boto3 import session
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from fastapi import HTTPException, status, UploadFile
from filetype.types import image
from filetype import guess

from src.domain.models.file import SupportedFileExtensions
from src.domain.schemas.file import FileBucketRead
from src.settings import settings


class FileBucketRepository:
    def __init__(self):
        self.max_image_size = 1024 * 1024 * 100  # 100 mb
        self.valid_image_types = (image.Jpeg, image.Png, image.Webp)
        s3_session = session.Session()
        self.s3 = s3_session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        chunk_size = 1024 * 1024
        self.transfer_config = TransferConfig(multipart_chunksize=chunk_size)

    async def get_presigned_url(self, file_name: str) -> FileBucketRead:
        try:
            response = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.bucket_name, 'Key': file_name},
            )
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail='Invalid credentials',
            ) from e
        return response

    async def upload(self, upload_file: UploadFile, key: str) -> FileBucketRead:
        if not self.check_file_valid(upload_file):
            raise HTTPException(status_code=400, detail="Недопустимый файла")

        self.s3.upload_fileobj(
            upload_file.file,
            settings.bucket_name,
            key,
            Config=self.transfer_config,
        )
        return await self.get_presigned_url(key)

    def check_file_valid(self, file: UploadFile) -> bool:
        image_type = guess(file.file)
        return file.size <= self.max_image_size and image_type.extension in [e.value for e in SupportedFileExtensions]

    async def delete(self, file_key: str) -> None:
        self.s3.delete_object(Bucket=settings.bucket_name, Key=file_key)
