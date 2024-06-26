from typing import Annotated

from pydantic import Field

from schemas.base import BaseSchema, IntID, NonEmptyString


class BaseEmployee(BaseSchema):
    name: Annotated[NonEmptyString, Field(max_length=64, examples=["John Doe"])]


class EmployeeRead(BaseEmployee):
    id: IntID
    studio_id: IntID
    user_id: IntID


class EmployeeCreate(BaseEmployee):
    user_id: IntID


class EmployeeUpdate(BaseEmployee): ...
