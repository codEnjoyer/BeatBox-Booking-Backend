from fastapi import HTTPException
from phonenumbers import (
    parse,
    is_valid_number,
    format_number,
    PhoneNumberFormat,
)
from starlette import status


def validate_number(number: str) -> str:
    try:
        phone_number = parse(number, 'RU')
        if not is_valid_number(phone_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid phone number: {phone_number}",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid phone number: {number}",
        )
    return format_number(phone_number, PhoneNumberFormat.NATIONAL)
