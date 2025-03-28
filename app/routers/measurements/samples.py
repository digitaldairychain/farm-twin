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
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from datetime import datetime
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/samples",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Sample(BaseModel):
    id: Optional[PyObjectId] = Field(
        alias="_id",
        default=None,
        json_schema_extra={
            'description': 'UUID of sensor',
            'example': str(ObjectId())
        })
    sensor: PyObjectId = Field(json_schema_extra={
        'description': 'UUID of sensor',
        'example': str(ObjectId())})
    timestamp:  Optional[datetime] = Field(default=None, json_schema_extra={
        'description': 'Time when sample recorded. Current time inserted'
                       + ' if empty',
        'example': str(datetime.now())})
    value: float = Field(json_schema_extra={
        'description': 'Value recorded by sensor',
        'example': 4.3})
    predicted: Optional[bool] = Field(default=False, json_schema_extra={
        'description': 'Flag if the value is a predicted value or not',
        'example': True})


class SampleCollection(BaseModel):
    samples: List[Sample]


@router.post(
    "/",
    response_description="Add new sample",
    response_model=Sample,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_samples(request: Request, samples: Sample):
    """
    Create a new sample if it does not already exist.

    Adds a timestamp if one is not included (useful for devices without an
    accurate clock).

    :param sample: Sample to be added
    """
    model = samples.model_dump(by_alias=True, exclude=["id"])
    if model["timestamp"] is None:
        model["timestamp"] = datetime.now()
    try:
        new_samples = await request.app.state.samples.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail=f"Sample {samples} already exists")
    if (
        created_samples := await
        request.app.state.samples.find_one({"_id": new_samples.inserted_id})
    ) is not None:
        return created_samples
    raise HTTPException(status_code=404, detail=f"Sample {samples._id}" +
                        " not successfully added")


@router.delete("/{id}", response_description="Delete a samples")
async def remove_samples(request: Request, id: str):
    """
    Delete a sample.

    :param id: UUID of the sample to delete
    """
    delete_result = await request.app.state.samples.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Sample {id} not found")


@router.get(
    "/",
    response_description="Search for samples",
    response_model=SampleCollection,
    response_model_by_alias=False,
)
async def sample_query(request: Request,
                       id: str | None = None,
                       sensor: str | None = None,
                       start: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
                       end: datetime | None = None,
                       predicted: bool | None = False):
    """
    Search for a sample given the provided criteria.

    :param id: Object ID of the sample
    :param sensor: Object ID of the sensor which generated this sample
    :param start: Timestamp from which to start the search
    :param end: Timestamp from which to end the search
    :param predicted: Whether or not the value is real or predicted
    """
    if id:
        id = ObjectId(id)
    if not end:
        end = datetime.now()
    query = {
        "_id": id,
        "sensor": sensor,
        "predicted": predicted
        }
    filtered_query = {k: v for k, v in query.items() if v is not None}
    filtered_query["timestamp"] = {"$gte": start, "$lte": end}
    result = await request.app.state.samples.find(filtered_query).to_list(1000)
    if len(result) > 0:
        return SampleCollection(samples=result)
    raise HTTPException(status_code=404, detail="No match found")
