from datetime import timedelta, datetime, timezone

import jwt

from src.settings import auth_settings


class AuthService:
    _jwt_secret_key: str

    def __init__(self, jwt_secret_key: str):
        self._jwt_secret_key = jwt_secret_key

    def create_access_token(self,
                            data: dict,
                            expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                hours=auth_settings.auth_token_expiration_hours)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(data,
                                 self._jwt_secret_key,
                                 algorithm=auth_settings.algorithm)
        return encoded_jwt

    def decode_jwt(self, token: str) -> dict:
        return jwt.decode(token,
                          self._jwt_secret_key,
                          algorithms=auth_settings.algorithm)
