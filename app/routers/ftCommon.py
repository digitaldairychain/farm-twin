from datetime import datetime
from typing import Optional

import pymongo
from fastapi import HTTPException, Path, Response, status
from pydantic import BaseModel, ConfigDict, Field, PastDatetime
from pydantic_extra_types import mongo_object_id


class FTModel(BaseModel):
    """farm-twin common model parameters."""

    ft: Optional[mongo_object_id.MongoObjectId] = Field(
        alias="_id", default=None, frozen=True
    )
    predicted: Optional[bool] = Field(
        default=False,
        json_schema_extra={
            "description": "Flag if the value is a predicted value or not",
            "example": True,
        },
    )
    created: PastDatetime = Path(default_factory=datetime.now, frozen=True)
    modified: PastDatetime = Path(default_factory=datetime.now)
    model_config = ConfigDict(extra="forbid")


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
        return {"$gte": start, "$lte": end}
    elif start and not end:
        return {"$gte": start, "$lte": datetime.now}
    elif not start and end:
        return {"$gte": datetime(1970, 1, 1, 0, 0, 0), "$lte": end}
    else:
        return {}


async def add_one_to_db(model, db, error_msg_object: str):
    model = model.model_dump(
        by_alias=True, exclude=["ft", "resourceType", "created", "modified"]
    )
    try:
        new = await db.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=404, detail=f"{error_msg_object} already exists"
        )
    if (created := await db.find_one({"_id": new.inserted_id})) is not None:
        return created
    raise HTTPException(
        status_code=404, detail=f"{error_msg_object} not successfully added"
    )


async def delete_one_from_db(db, ft: mongo_object_id, error_msg_object: str):
    delete_result = await db.delete_one({"_id": ft})
    print(ft)
    print(delete_result.deleted_count)
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"{error_msg_object} {ft} not found")


async def find_in_db(db, query: dict):
    result = await db.find(filterQuery(query)).to_list(1000)

    if len(result) > 0:
        return result

    raise HTTPException(status_code=404, detail="No match found")


async def update_one_in_db(model, db, ft: mongo_object_id, error_msg_object: str):
    await db.update_one(
        {"_id": ft},
        {
            "$set": model.model_dump(
                by_alias=True, exclude=["ft", "resourceType", "created", "modified"]
            )
        },
        upsert=False,
    )
    if (updated := await db.find_one({"_id": ft})) is not None:
        return updated
    raise HTTPException(
        status_code=404, detail=f"{error_msg_object} {ft} not successfully updated"
    )
