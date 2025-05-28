from pydantic import BaseModel, Field, PastDatetime
from typing import Optional

from pydantic_extra_types import mongo_object_id
from datetime import datetime
from fastapi import Path
from bson.objectid import ObjectId
from bson.errors import InvalidId


class FTModel(BaseModel):
    """farm-twin common model parameters."""
    ft: Optional[mongo_object_id.MongoObjectId] = Field(
        alias="_id",
        default=None,
        frozen=True
    )
    created: PastDatetime = Path(default_factory=datetime.now, frozen=True)
    modified:  PastDatetime = Path(default_factory=datetime.now)
    predicted: Optional[bool] = Field(
        default=False,
        json_schema_extra={
            "description": "Flag if the value is a predicted value or not",
            "example": True,
        },
    )


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


def filterQuery(query: dict):
    filtered_query = {}
    for k, v in query.items():
        if v is not None:
            if isinstance(v, dict):
                v = filterQuery(v)
            if v:
                filtered_query[k] = v
    return filtered_query
