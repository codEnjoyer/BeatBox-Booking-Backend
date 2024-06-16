from typing import Annotated

from fastapi import Query, Path
from pydantic import PositiveInt, NonNegativeInt

PathIntID = Annotated[PositiveInt, Path(ge=1)]
QueryLimit = Annotated[PositiveInt, Query(gt=0, le=1000)]
QueryOffset = Annotated[NonNegativeInt, Query(ge=0, le=1_000_000)]
