from datetime import datetime
from typing import Optional

from fastapi import Path
from pydantic import BaseModel, ConfigDict, Field, PastDatetime
from pydantic_extra_types import mongo_object_id


class FTModel(BaseModel):
    """farm-twin common model parameters."""
    ft: Optional[mongo_object_id.MongoObjectId] = Field(
        alias="_id",
        default=None,
        frozen=True
    )
    predicted: Optional[bool] = Field(
        default=False,
        json_schema_extra={
            "description": "Flag if the value is a predicted value or not",
            "example": True,
        },
    )
    created: PastDatetime = Path(default_factory=datetime.now, frozen=True)
    modified:  PastDatetime = Path(default_factory=datetime.now)
    model_config = ConfigDict(extra='forbid')


def filterQuery(query: dict):
    filtered_query = {}
    for k, v in query.items():
        if v is not None:
            if isinstance(v, dict):
                v = filterQuery(v)
            if v:
                filtered_query[k] = v
    return filtered_query


def dateBuild(start: datetime, end: datetime):
    if start and end:
        return {"$gte": start,
                "$lte": end}
    elif start and not end:
        return {"$gte": start,
                "$lte": datetime.now}
    elif not start and end:
        return {"$gte": datetime(1970, 1, 1, 0, 0, 0),
                "$lte": end}
    else:
        return {}
