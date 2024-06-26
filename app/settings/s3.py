from pydantic import Field

from settings.base import CommonBaseSettings


class S3Settings(CommonBaseSettings):
    endpoint: str = Field(validation_alias="S3_ENDPOINT")
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str


s3_settings = S3Settings()
