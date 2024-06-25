from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    environment: Literal[
        "PROD", "TEST"
    ]  # PROD / TEST. ENVIRONMENT=TEST используется для проверки в тестах.

    db_host: str
    db_port: int
    db_pass: str
    db_name: str
    db_user: str

    app_port: int
    root_password: str

    s3_endpoint: str
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str

    app_host: str = "0.0.0.0"

    @property
    def database_url(self) -> str:
        host = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )
        return str(host)


settings = Settings()


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    secret_auth_token: str
    auth_token_expiration_hours: int
    algorithm: str = "HS256"


auth_settings = AuthSettings()
