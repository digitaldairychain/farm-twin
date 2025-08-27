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

from bson.objectid import ObjectId
from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from ..ftCommon import (FTModel, add_one_to_db, dateBuild, delete_one_from_db,
                        find_in_db)

router = APIRouter(
    prefix="/samples",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Sample"


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
    return await add_one_to_db(sample, request.app.state.samples, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete a samples")
async def remove_samples(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a sample.

    :param ft: ObjectID of the sample to delete
    """
    return await delete_one_from_db(request.app.state.samples, ft, ERROR_MSG_OBJECT)


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
    timestampStart: datetime | None = None,
    timestampEnd: datetime | None = None,
    predicted: bool | None = False,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a sample given the provided criteria."""
    query = {
        "_id": ft,
        "sensor": sensor,
        "predicted": predicted,
        "timestamp": dateBuild(timestampStart, timestampEnd),
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId
    }
    result = await find_in_db(request.app.state.samples, query)
    return SampleCollection(samples=result)
