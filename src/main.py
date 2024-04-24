from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.models.user import User

app = FastAPI(title="BeatBox Booking Backend", version="0.0.1")


@app.get("/users")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@app.post("/users")
async def create_user(user: dict, session: AsyncSession = Depends(get_async_session)):
    session.add(User(**user))
    result = await session.commit()
    return result