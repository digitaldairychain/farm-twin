"""
Collects API calls related to sampled weights for a group of animals.

The weight of animals may be measured periodically by devices stationed
on the farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarGroupWeightEventResource.json
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from ...ftCommon import dateBuild, filterQuery
from ...icar import icarEnums
from ...icar.icarResources import icarGroupWeightEventResource as GroupWeight

router = APIRouter(
    prefix="/group_weight",
    tags=["events", "performance"],
    responses={404: {"description": "Not found"}},
)


class GroupWeightCollection(BaseModel):
    group_weight: List[GroupWeight]


@router.post(
    "/",
    response_description="Add group weight event",
    response_model=GroupWeight,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_group_weight_event(request: Request, group_weight: GroupWeight):
    """
    Create a new group weight event.

    Adds a timestamp if one is not included (useful for devices without an
    accurate clock).

    :param group_weight: Group weight to be added
    """
    model = group_weight.model_dump(by_alias=True, exclude=["ft", "resourceType"])
    try:
        new_we = await request.app.state.group_weight.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=404, detail=f"Group Weight {group_weight} already exists"
        )
    if (
        created_group_weight_event := await request.app.state.group_weight.find_one(
            {"_id": new_we.inserted_id}
        )
    ) is not None:
        return created_group_weight_event
    raise HTTPException(
        status_code=404, detail="Group weight event not successfully" + " added"
    )


@router.delete("/{ft}", response_description="Delete a group weight event")
async def remove_group_weight_event(request: Request, ft: str):
    """
    Delete a weight event.

    :param ft: ObjectID of the group weight event to delete
    """
    delete_result = await request.app.state.group_weight.delete_one(
        {"_id": ObjectId(ft)}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Group weight event {ft} not found")


@router.get(
    "/",
    response_description="Search for group weight event",
    response_model=GroupWeightCollection,
    response_model_by_alias=False,
)
async def group_weight_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    method: icarEnums.icarWeightMethodType | None = None,
    animal: str | None = None,
    device: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a groupweight event given the provided criteria."""
    query = {
        "_id": ft,
        "method": method,
        "animal.id": animal,
        "device.id": device,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await request.app.state.group_weight.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return GroupWeightCollection(group_weight=result)
    raise HTTPException(status_code=404, detail="No match found")
