"""
Collects API calls related to animal weight events.

The weight of animals may be measured periodically by devices stationed
on the farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarWeightEventResource.json
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from ..ftCommon import dateBuild, filterQuery
from ..icar.icarResources import icarWeightEventResource as Weight

router = APIRouter(
    prefix="/weight",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


class WeightCollection(BaseModel):
    weight: List[Weight]


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
    try:
        new_we = await request.app.state.weights.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404, detail=f"Weight {weight} already exists")
    if (
        created_weight_event := await request.app.state.weights.find_one(
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

    :param ft: ObjectID of the weight event to delete
    """
    delete_result = await request.app.state.weights.delete_one({"_id": ObjectId(ft)})

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
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    device: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a weight event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "device.id": device,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await request.app.state.weights.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return WeightCollection(weight=result)
    raise HTTPException(status_code=404, detail="No match found")
