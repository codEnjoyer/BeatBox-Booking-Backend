import pytest
from fastapi import status
from httpx import AsyncClient

from app.domain.schemas.user import UserCreate


@pytest.mark.usefixtures("clear_database")
class TestAuth:
    user_schema = UserCreate(
        username="test", email="test@example.com", hashed_password="test-pass"
    )

    async def test_register(self, async_client: AsyncClient):

        response = await async_client.post(
            "/users",
            json={
                "username": self.user_schema.username,
                "email": self.user_schema.email,
                "hashed_password": self.user_schema.hashed_password,
            },  # ToDo: сделать через **user_schema.model_dump()
        )

        assert (
            response.status_code == status.HTTP_201_CREATED
        ), "Зарегистрировать пользователя не удалось"

        assert response.json()["username"] == self.user_schema.username
        assert response.json()["email"] == self.user_schema.email

    async def test_login(self, async_client: AsyncClient):
        # Регистрация пользователя в пустой базе данных путём вызова первого теста
        await self.test_register(async_client=async_client)

        response = await async_client.post(
            "/users/auth",
            json={
                "username": self.user_schema.username,
                "hashed_password": self.user_schema.hashed_password,
            },
        )

        assert (
            response.status_code == status.HTTP_200_OK
        ), "Не удалось авторизовать пользователя"

        assert response.json()["username"] == self.user_schema.username
        assert response.json()["email"] == self.user_schema.email
