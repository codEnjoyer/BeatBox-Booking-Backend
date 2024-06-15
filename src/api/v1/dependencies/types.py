from typing import Annotated

from fastapi import Query
from pydantic import PositiveInt, NonNegativeInt

QueryLimit = Annotated[PositiveInt, Query(gt=0, le=1000)]
QueryOffset = Annotated[NonNegativeInt, Query(ge=0, le=1_000_000)]
