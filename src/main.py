from contextlib import asynccontextmanager

from sqlalchemy.exc import NoResultFound, IntegrityError

from src.api import *  # noqa: F403
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException, status


def include_routers(app_: FastAPI, *routers: APIRouter) -> None:
    for routers in routers:
        app_.include_router(routers)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Запускаем код до и после запуска приложения"""
    include_routers(
        app_,
        auth_router,  # noqa: F405
        employee_router,  # noqa: F405
        file_router,  # noqa: F405
        review_router,  # noqa: F405
        studio_router,  # noqa: F405
        user_router,  # noqa: F405
        room_router,  # noqa: F405
        booking_router,  # noqa: F405
    )
    yield  # Возвращаем работу приложению
    # Тут можно выполнить код после завершения приложения


app = FastAPI(
    root_path="/api",
    title="BeatBox Booking Backend",
    version="0.0.1",
    lifespan=lifespan,
)


@app.exception_handler(NoResultFound)
async def not_found_handler(_: Request, exc: NoResultFound) -> Response:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Requested item was not found",
    ) from exc


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_: Request, exc: IntegrityError) -> Response:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Data is invalid",
    ) from exc
