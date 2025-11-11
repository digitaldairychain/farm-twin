"""
Collects API calls related to an animal being dried off at the end of a lactation.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarMilkingDryOffEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import add_one_to_db, dateBuild, delete_one_from_db, find_in_db
from ...icar.icarResources import icarMilkingDryOffEventResource as DryingOff
from ...users import User, get_current_active_user

ERROR_MSG_OBJECT = "Drying Off"

router = APIRouter(
    prefix="/drying_off",
    tags=["milking"],
    responses={404: {"description": "Not found"}},
)


class DryingOffCollection(BaseModel):
    drying_off: List[DryingOff]


@router.post(
    "/",
    response_description="Add drying off event",
    response_model=DryingOff,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_drying_off_event(
    request: Request,
    drying_off: DryingOff,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_milking"])
    ],
):
    """
    Create a new drying off event.

    :param drying_off: Drying off to be added
    """
    return await add_one_to_db(
        drying_off, request.app.state.drying_off, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a drying off event")
async def remove_drying_off_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_milking"])
    ],
):
    """
    Delete a drying off event.

    :param ft: ObjectID of the drying off event to delete
    """
    return await delete_one_from_db(request.app.state.drying_off, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for drying off event",
    response_model=DryingOffCollection,
    response_model_by_alias=False,
)
async def drying_off_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_milking"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a drying off event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.drying_off, query)
    return DryingOffCollection(drying_off=result)
