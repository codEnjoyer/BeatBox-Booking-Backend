from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from settings.base import CommonBaseSettings


class DatabaseSettings(CommonBaseSettings):
    db_host: str
    db_port: int
    db_pass: str
    db_name: str
    db_user: str

    @property
    def url(self) -> str:
        host = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )
        return str(host)


db_settings = DatabaseSettings()


class TestDatabaseSettings(DatabaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../test.env", env_file_encoding="utf-8", extra="allow"
    )


test_db_settings = TestDatabaseSettings()
