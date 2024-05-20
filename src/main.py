from contextlib import asynccontextmanager

from sqlalchemy.exc import NoResultFound

from src.api import *  # noqa: F403
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException, status


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
    )
    yield  # Возвращаем работу приложению
    # Тут можно выполнить код после завершения приложения


app = FastAPI(
    title="BeatBox Booking Backend", version="0.0.1", lifespan=lifespan
)


@app.exception_handler(NoResultFound)
async def not_found_handler(_: Request, exc: NoResultFound) -> Response:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Requested item was not found",
    ) from exc
