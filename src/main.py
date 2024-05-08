from contextlib import asynccontextmanager

from fastapi import FastAPI

# Настройки для JWT-токенов
SECRET = "my_super_secret_key"
TOKEN_URL = "/auth/login"

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Запускаем код до и после запуска приложения"""
    # Тут можно выполнить код до запуска приложения: различные include_router, и другие доп. настройки/проверки
    yield  # Возвращаем работу приложению
    # Тут можно выполнить код после завершения приложения


app = FastAPI(title="BeatBox Booking Backend", version="0.0.1", lifespan=lifespan)
