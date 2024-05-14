from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    mode: Literal["ANY", "TEST"]  # ANY / TEST. MODE=TEST используется для проверки в тестах.

    db_host: str
    db_port: int
    db_pass: str
    db_name: str
    db_user: str

    secret_auth_token: str

    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str

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
print(f"Settings Mode: {settings.mode}")
