from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from phonenumbers import (
    parse,
    is_valid_number,
    format_number,
    PhoneNumberFormat,
)
from starlette import status

from src.domain.models.user import User
from src.domain.schemas.user import UserCreateSchema
from src.domain.dependencies.auth import hash_password


async def create_user(
    user_schema: UserCreateSchema, session: AsyncSession
) -> User:
    phone_number = parse(user_schema.phone_number, 'RU')
    if not is_valid_number(phone_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid phone number: {user_schema.phone_number}",
        )
    formatted_number = format_number(phone_number, PhoneNumberFormat.NATIONAL)
    new_user = User(
        email=user_schema.email,
        hashed_password=hash_password(user_schema.password),
        is_superuser=user_schema.is_superuser,
        phone_number=formatted_number,
    )
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    await session.commit()
    return new_user
