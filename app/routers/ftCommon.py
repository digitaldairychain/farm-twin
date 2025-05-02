from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]


class FTModel(BaseModel):
    """farm-twin common model parameters."""
    ft: Optional[PyObjectId] = Field(
        alias="_id",
        default=None,
    )
    created:  Optional[datetime] = Field(default=None)
    modified:  Optional[datetime] = Field(default=None)


class modified():
    """Object to represent parameters when searching for modified objects."""
    search = True
    start = None
    end = None


def modifiedFilter(modifiedStart, modifiedEnd):
    """Parse parameters when search for modified objects. """
    mod = modified()
    if not modifiedEnd and not modifiedStart:
        mod.search = False
    if not modifiedEnd:
        mod.end = datetime.now()
    if not modifiedStart:
        mod.start = datetime(1970, 1, 1, 0, 0, 0)
    return mod
