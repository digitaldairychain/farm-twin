from pydantic import BaseModel, Field, PastDatetime
from typing import Optional
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from datetime import datetime
from fastapi import Path
from bson.objectid import ObjectId
from bson.errors import InvalidId

PyObjectId = Annotated[str, BeforeValidator(str)]


class FTModel(BaseModel):
    """farm-twin common model parameters."""
    ft: Optional[PyObjectId] = Field(
        alias="_id",
        default=None,
        frozen=True
    )
    created: PastDatetime = Path(default_factory=datetime.now, frozen=True)
    modified:  PastDatetime = Path(default_factory=datetime.now)


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


def checkObjectId(ft: str):
    try:
        oid = ObjectId(ft)
        if str(oid) == ft:
            return ObjectId(ft)
    except (InvalidId, TypeError) as e:
        raise e
