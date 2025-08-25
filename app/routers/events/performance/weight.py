"""
Collects API calls related to animal weight events.

The weight of animals may be measured periodically by devices stationed
on the farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarWeightEventResource.json
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         filterQuery, find_in_db)
from ...icar.icarResources import icarWeightEventResource as Weight

router = APIRouter(
    prefix="/weight",
    tags=["performance"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Weight"


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
    return await add_one_to_db(weight, request.app.state.weight, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete a weight event")
async def remove_weight_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a weight event.

    :param ft: ObjectID of the weight event to delete
    """
    return await delete_one_from_db(request.app.state.weight, ft, ERROR_MSG_OBJECT)


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
    result = await find_in_db(request.app.state.weight, query)
    return WeightCollection(weight=result)
