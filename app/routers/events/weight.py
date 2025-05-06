"""
Collects API calls related to animal weight events.

The weight of animals may be measured periodically by devices stationed
on the farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarWeightEventResource.json
"""
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request, Query
from pydantic import BaseModel, Field, AfterValidator
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from datetime import datetime
from bson.objectid import ObjectId
from ..icar import icarTypes
from ..ftCommon import FTModel, checkObjectId

router = APIRouter(
    prefix="/weight",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

PyObjectId = Annotated[str, BeforeValidator(str)]


class Weight(FTModel):
    weight: icarTypes.icarMassMeasureType = Field(
        json_schema_extra={
            "description": "The weight measurement, including units and "
            + "resolution.",
        }
    )
    animal: PyObjectId = Field(
        json_schema_extra={
            "description": "ObjectID of animal.",
            "example": str(ObjectId()),
        }
    )
    device: Optional[PyObjectId] = Field(
        default=None,
        json_schema_extra={
            "description": "ObjectID of device.",
            "example": str(ObjectId()),
        },
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            "description": "Time when weight recorded. Current time inserted"
            + " if empty",
            "example": str(datetime.now()),
        },
    )
    timeOffFeed: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Hours of curfew or withholding feed prior to"
            + " weighing to standardise gut fill.",
        },
    )
    predicted: Optional[bool] = Field(
        default=False,
        json_schema_extra={
            "description": "Flag if the value is a predicted value or not",
            "example": True,
        },
    )


class WeightCollection(BaseModel):
    weights: List[Weight]


@router.post(
    "/",
    response_description="Add weight event",
    response_model=Weight,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_weight_event(request: Request, weight: Weight):
    """
    Create a new weight event.

    Adds a timestamp if one is not included (useful for devices without an
    accurate clock).

    :param weight: Weight to be added
    """
    model = weight.model_dump(by_alias=True, exclude=["ft"])
    if model["timestamp"] is None:
        model["timestamp"] = datetime.now()
    try:
        new_we = await request.app.state.weight.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail=f"Weight {weight} already exists")
    if (
        created_weight_event := await request.app.state.weight.find_one(
            {"_id": new_we.inserted_id}
        )
    ) is not None:
        return created_weight_event
    raise HTTPException(
        status_code=404, detail="Weight event not successfully" + " added"
    )


@router.delete("/{ft}", response_description="Delete a weight event")
async def remove_weight_event(request: Request, ft: str):
    """
    Delete a weight event.

    :param ft: UUID of the weight event to delete
    """
    delete_result = await request.app.state.weight.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Weight event {ft} not found")


@router.get(
    "/",
    response_description="Search for weight event",
    response_model=WeightCollection,
    response_model_by_alias=False,
)
async def weight_event_query(
    request: Request,
    ft: Annotated[str | None, AfterValidator(checkObjectId)] = None,
    device: Annotated[str | None, AfterValidator(checkObjectId)] = None,
    start: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    end: Annotated[datetime, Query(default_factory=datetime.now)] = None,
    createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
):
    """Search for a weight event given the provided criteria."""
    query = {
        "_id": ft,
        "device": device,
        "timestamp": {"$gte": start, "$lte": end},
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": createdStart, "$lte": createdEnd},
    }
    filtered_query = {k: v for k, v in query.items() if v is not None}
    result = await request.app.state.weight.find(filtered_query).to_list(1000)
    if len(result) > 0:
        return WeightCollection(weights=result)
    raise HTTPException(status_code=404, detail="No match found")
