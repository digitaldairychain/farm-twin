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
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import add_one_to_db, dateBuild, delete_one_from_db, find_in_db
from ...icar import icarEnums
from ...icar.icarResources import icarGroupWeightEventResource as GroupWeight
from ...users import User, get_current_active_user

router = APIRouter(
    prefix="/group_weight",
    tags=["performance"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Group Weight"


class GroupWeightCollection(BaseModel):
    group_weight: List[GroupWeight]


@router.post(
    "/",
    response_description="Add group weight event",
    response_model=GroupWeight,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_group_weight_event(
    request: Request,
    group_weight: GroupWeight,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_performance"])
    ],
):
    """
    Create a new group weight event.

    Adds a timestamp if one is not included (useful for devices without an
    accurate clock).

    :param group_weight: Group weight to be added
    """
    return await add_one_to_db(
        group_weight, request.app.state.group_weight, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a group weight event")
async def remove_group_weight_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_performance"])
    ],
):
    """
    Delete a weight event.

    :param ft: ObjectID of the group weight event to delete
    """
    return await delete_one_from_db(
        request.app.state.group_weight, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for group weight event",
    response_model=GroupWeightCollection,
    response_model_by_alias=False,
)
async def group_weight_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_performance"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    method: icarEnums.icarWeightMethodType | None = None,
    animal: str | None = None,
    device: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a groupweight event given the provided criteria."""
    query = {
        "_id": ft,
        "method": method,
        "animal.id": animal,
        "device.id": device,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.group_weight, query)
    return GroupWeightCollection(group_weight=result)
