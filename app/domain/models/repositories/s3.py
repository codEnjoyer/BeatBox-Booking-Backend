import aioboto3
from aiohttp import ClientError
from fastapi import UploadFile

from app.domain.exceptions.file import FileNotFoundException
from app.settings import settings

CHUNK_SIZE = 1024 * 1024  # 1 Mb
URL_EXPIRES_IN_SECONDS = 60 * 60  # 1 hour


class S3Repository:
    def __init__(self):
        self.service_name = 's3'
        self.endpoint = settings.s3_endpoint
        self.bucket_name = settings.bucket_name
        self.session = aioboto3.Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    async def get_url(self, filename: str) -> str:
        async with self.session.client(
            self.service_name, endpoint_url=self.endpoint
        ) as client:
            try:
                url = await client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': filename},
                    ExpiresIn=URL_EXPIRES_IN_SECONDS,
                )
            except ClientError as e:
                raise FileNotFoundException from e
        return url

    async def upload(self, file: UploadFile, filename: str) -> str:
        async with self.session.client(
            self.service_name, endpoint_url=self.endpoint
        ) as client:
            await client.upload_fileobj(file, self.bucket_name, filename)
        return filename

    async def delete(self, filename: str) -> None:
        async with self.session.client(
            self.service_name, endpoint_url=self.endpoint
        ) as client:
            await client.delete_object(Bucket=self.bucket_name, Key=filename)
