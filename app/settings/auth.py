from pydantic import Field

from settings.base import CommonBaseSettings


class AuthSettings(CommonBaseSettings):
    secret_token: str = Field(validation_alias="SECRET_AUTH_TOKEN")
    token_expiration_hours: int = Field(
        validation_alias="AUTH_TOKEN_EXPIRATION_HOURS"
    )
    algorithm: str = "HS256"


auth_settings = AuthSettings()
