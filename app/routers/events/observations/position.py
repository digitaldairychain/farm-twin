"""
Collects API calls related to animal position observation events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarPositionObservationEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar import icarEnums
from ...icar.icarResources import \
    icarPositionObservationEventResource as Position

ERROR_MSG_OBJECT = "Position"

router = APIRouter(
    prefix="/position",
    tags=["observations", "position"],
    responses={404: {"description": "Not found"}},
)


class PositionCollection(BaseModel):
    position: List[Position]


@router.post(
    "/",
    response_description="Add position observation event",
    response_model=Position,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_position_event(request: Request, position: Position):
    """
    Create a new position event.

    :param position: Position to be added
    """
    model = position.model_dump(by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(model, request.app.state.position, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_position_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a position event.

    :param ft: ObjectID of the position event to delete
    """
    return await delete_one_from_db(request.app.state.position, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for position event",
    response_model=PositionCollection,
    response_model_by_alias=False,
)
async def position_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a position event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.position, query)
    return PositionCollection(position=result)
