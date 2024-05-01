from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    mode: str  # ANY / TEST. MODE=TEST используется для проверки в тестах.

    db_host: str
    db_port: int
    db_pass: str
    db_name: str
    db_user: str

    @property
    def database_url(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        ).__str__()


settings = Settings()
print(f"Settings Mode: {settings.mode}")
