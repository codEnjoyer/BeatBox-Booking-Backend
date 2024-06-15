from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema


class BaseEmployee(BaseSchema): ...


class EmployeeRead(BaseEmployee):
    id: PositiveInt
    studio_id: PositiveInt
    user: "UserRead"


class EmployeeCreate(BaseEmployee):
    name: str = Field(min_length=3)
    user_id: PositiveInt


class EmployeeUpdate(BaseEmployee):
    name: str = Field(min_length=3)


from src.domain.schemas.user import UserRead

EmployeeRead.update_forward_refs()
