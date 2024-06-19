from typing import Annotated
import datetime

from fastapi import Query, Path
from pydantic import PositiveInt, NonNegativeInt

PathIntID = Annotated[PositiveInt, Path(ge=1)]
QueryLimit = Annotated[PositiveInt, Query(gt=0, le=1000)]
QueryOffset = Annotated[NonNegativeInt, Query(ge=0, le=1_000_000)]
QueryDateFrom = Annotated[datetime.date, Query(
    description="Включительно",
    example="2024-06-16")]
QueryDateTo = Annotated[datetime.date, Query(
    description="Не включительно",
    examples=["2024-06-18"])]
