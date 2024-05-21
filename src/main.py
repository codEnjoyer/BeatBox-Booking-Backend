from contextlib import asynccontextmanager
from src.api import *  # noqa: F403
from fastapi import FastAPI, APIRouter


def include_routers(app_: FastAPI, *routers: APIRouter) -> None:
    for routers in routers:
        app_.include_router(routers)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Запускаем код до и после запуска приложения"""
    include_routers(
        fastapi_app,
        auth_router,  # noqa: F405
        studio_router,  # noqa: F405
        user_router,  # noqa: F405
        file_router,  # noqa: F405
        review_router,  # noqa: F405
        room_router,  # noqa: F405
        booking_router,  # noqa: F405
    )
    yield  # Возвращаем работу приложению
    # Тут можно выполнить код после завершения приложения


app = FastAPI(
    title="BeatBox Booking Backend", version="0.0.1", lifespan=lifespan
)
