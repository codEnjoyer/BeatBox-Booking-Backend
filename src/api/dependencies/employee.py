from fastapi import HTTPException, status

from src.api.dependencies.auth import AuthenticatedUser
from src.domain.models import User


def can_create_employee(user: AuthenticatedUser) -> User:
    can_create = user.is_superuser or user.employee is not None
    if not can_create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    return user
