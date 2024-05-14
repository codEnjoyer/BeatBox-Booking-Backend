from contextlib import asynccontextmanager
from src.api import *
from fastapi import FastAPI, APIRouter


def include_routers(app_: FastAPI, *routers: APIRouter) -> None:
    for routers in routers:
        app_.include_router(routers)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Запускаем код до и после запуска приложения"""
    include_routers(
        fastapi_app, auth_router, studio_router, user_router, file_router
    )
    yield  # Возвращаем работу приложению
    # Тут можно выполнить код после завершения приложения


app = FastAPI(
    title="BeatBox Booking Backend", version="0.0.1", lifespan=lifespan
)
