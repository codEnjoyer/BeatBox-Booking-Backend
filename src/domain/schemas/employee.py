from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema
from src.domain.schemas.studio import StudioRead
from src.domain.schemas.user import UserRead


class BaseEmployee(BaseSchema): ...


class EmployeeRead(BaseEmployee):
    id: PositiveInt
    user: UserRead
    studio: StudioRead


class EmployeeCreate(BaseEmployee):
    name: str = Field(min_length=3)
    studio_id: PositiveInt
    user_id: PositiveInt


class EmployeeUpdate(BaseEmployee):
    name: str = Field(min_length=3)
