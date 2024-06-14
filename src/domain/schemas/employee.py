from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema


class BaseEmployee(BaseSchema):
    studio_id: PositiveInt
    user_id: PositiveInt


class EmployeeRead(BaseEmployee):
    id: PositiveInt


class EmployeeCreate(BaseEmployee):
    name: str = Field(min_length=3)


class EmployeeUpdate(BaseSchema):
    name: str = Field(min_length=3)
