"""
Collects API calls related to samples.

Samples are single measurements, taken from a sensor.

A sensor will produce multiple samples over its lifetime.

A sample includes the value recorded and the time at which it was recorded.

A sample can also be real or predicted, and should be tagged as such.

An on-farm example is an outdoor temperature sample.

This collection of endpoints allows for the addition, deletion
and finding of those samples.
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import FTModel, filterQuery

router = APIRouter(
    prefix="/samples",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


class Sample(FTModel):
    sensor: mongo_object_id.MongoObjectId = Field(
        json_schema_extra={
            "description": "ObjectID of sensor",
            "example": str(ObjectId()),
        }
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            "description": "Time when sample recorded. Current time inserted"
            + " if empty",
            "example": str(datetime.now()),
        },
    )
    value: float = Field(
        json_schema_extra={
            "description": "Value recorded by sensor",
            "example": 4.3,
        }
    )
    predicted: Optional[bool] = Field(
        default=False,
        json_schema_extra={
            "description": "Flag if the value is a predicted value or not",
            "example": True,
        },
    )


class SampleCollection(BaseModel):
    samples: List[Sample]


@router.post(
    "/",
    response_description="Add new sample",
    response_model=Sample,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_sample(request: Request, sample: Sample):
    """
    Create a new sample if it does not already exist.

    Adds a timestamp if one is not included (useful for devices without an
    accurate clock).

    :param sample: Sample to be added
    """
    model = sample.model_dump(by_alias=True, exclude=["ft"])
    if model["timestamp"] is None:
        model["timestamp"] = datetime.now()
    try:
        new_sample = await request.app.state.samples.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=404, detail="Sample already exists"
        )
    if (
        created_sample := await request.app.state.samples.find_one(
            {"_id": new_sample.inserted_id}
        )
    ) is not None:
        return created_sample
    raise HTTPException(
        status_code=404,
        detail=f"Sample {new_sample.ft}" + " not successfully added",
    )


@router.delete("/{ft}", response_description="Delete a samples")
async def remove_samples(request: Request, ft: str):
    """
    Delete a sample.

    :param ft: ObjectID of the sample to delete
    """
    delete_result = await request.app.state.samples.delete_one(
        {"_id": ObjectId(ft)}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Sample {ft} not found")


@router.get(
    "/",
    response_description="Search for samples",
    response_model=SampleCollection,
    response_model_by_alias=False,
)
async def sample_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    sensor: mongo_object_id.MongoObjectId | None = None,
    start: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    end: Annotated[datetime, Query(default_factory=datetime.now)] = None,
    predicted: bool | None = False,
    createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(default_factory=datetime.now)] = None
):
    """Search for a sample given the provided criteria."""
    query = {
        "_id": ft,
        "sensor": sensor,
        "predicted": predicted,
        "timestamp": {"$gte": start, "$lte": end},
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": createdStart, "$lte": createdEnd}
    }
    result = await request.app.state.samples.find(
        filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return SampleCollection(samples=result)
    raise HTTPException(status_code=404, detail="No match found")
