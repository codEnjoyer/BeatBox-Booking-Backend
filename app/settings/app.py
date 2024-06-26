from typing import Literal

from pydantic import Field

from settings.base import CommonBaseSettings


class AppSettings(CommonBaseSettings):
    environment: Literal[
        "PROD", "DEV", "TEST"
    ]  # PROD / TEST. ENVIRONMENT=TEST используется для проверки в тестах.

    port: int = Field(validation_alias="APP_PORT")
    root_password: str

    host: str = "0.0.0.0"


app_settings = AppSettings()
