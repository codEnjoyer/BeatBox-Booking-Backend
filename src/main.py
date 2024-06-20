from contextlib import asynccontextmanager

from src.api import v1_router
from fastapi import FastAPI, Request, Response, HTTPException, status

from src.data.demo import load_demo_data
from src.data.initial import load_initial_data
from src.domain.exceptions.base import BBBException
from src.settings import settings


@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Запускаем код до и после запуска приложения"""
    await load_initial_data()
    if settings.environment == "PROD":
        await load_demo_data()
    app_.include_router(v1_router)
    yield  # Возвращаем работу приложению
    # Тут можно выполнить код после завершения приложения


app = FastAPI(
    root_path="/api",
    title="BeatBox Booking Backend",
    version="0.0.1",
    lifespan=lifespan,
)


@app.exception_handler(BBBException)
async def service_exception_handler(_: Request, exc: BBBException) -> Response:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
    ) from exc
