from contextlib import asynccontextmanager

from sqlalchemy.exc import NoResultFound

from src.api import v1_router
from fastapi import FastAPI, Request, Response, HTTPException, status


@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Запускаем код до и после запуска приложения"""
    app_.include_router(v1_router)
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
