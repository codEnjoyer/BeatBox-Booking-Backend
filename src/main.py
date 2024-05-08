from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.models.user import User
from src.schemas.user import UserReadSchema, UserCreateSchema, UserAuthSchema


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Запускаем код до и после запуска приложения"""
    # Тут можно выполнить код до запуска приложения: различные include_router, и другие доп. настройки/проверки
    yield  # Возвращаем работу приложению
    # Тут можно выполнить код после завершения приложения


app = FastAPI(title="BeatBox Booking Backend", version="0.0.1", lifespan=lifespan)


@app.get("/users", response_model=list[UserReadSchema])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@app.post("/users", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_schema: UserCreateSchema, session: AsyncSession = Depends(get_async_session)
):
    new_user = User(**user_schema.model_dump())
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    await session.commit()
    return new_user


@app.post("/users/auth", response_model=UserReadSchema)
async def auth_user(
    user_schema: UserAuthSchema, session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = select(User)
        stmt = stmt.filter_by(
            username=user_schema.username, hashed_password=user_schema.hashed_password
        )
        result = await session.execute(stmt)

        return result.unique().scalar_one()

    except NoResultFound:
        # Обработка случая, когда пользователь не найден
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
