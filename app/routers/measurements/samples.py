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
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    device: str
    sensor: PyObjectId
    timestamp:  Optional[datetime] = Field(default=None)
    value: float
    predicted: Optional[bool] = Field(default=False)


class SampleCollection(BaseModel):
    samples: List[Sample]


@router.post(
    "/",
    response_description="Add new samples",
    response_model=Sample,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_samples(request: Request, samples: Sample):
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
    delete_result = await request.app.state.samples.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Sample {id} not found")


@router.get(
    "/{id}",
    response_description="Get a single samples point",
    response_model=Sample,
    response_model_by_alias=False,
)
async def list_samples_single(request: Request, id: str):
    if (
        samples := await request.app.state.samples.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return samples

    raise HTTPException(status_code=404, detail=f"Sample {id} not found")


@router.get(
    "/bysensor/",
    response_description="Get samples by sensor tag",
    response_model=SampleCollection,
    response_model_by_alias=False,
)
async def list_samples_coordinates(request: Request, tag: str):
    return SampleCollection(locations=await
                            request.app.state.samples.find(
                                {"tag": tag}).to_list(1000))
# TODO: Should allow queries for a date range
