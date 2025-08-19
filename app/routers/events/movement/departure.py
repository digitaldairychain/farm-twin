"""
Collects API calls related to animal departure events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarMovementDepartureEventResource.json
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
    icarMovementDepartureEventResource as Departure

ERROR_MSG_OBJECT = "Departure"

router = APIRouter(
    prefix="/departure",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)


class DepartureCollection(BaseModel):
    departure: List[Departure]


@router.post(
    "/",
    response_description="Add departure event",
    response_model=Departure,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_departure_event(request: Request, departure: Departure):
    """
    Create a new departure event.

    :param departure: Departure to be added
    """
    model = departure.model_dump(by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(model, request.app.state.departure, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_departure_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a departure event.

    :param ft: ObjectID of the departure event to delete
    """
    return await delete_one_from_db(request.app.state.departure, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for departure event",
    response_model=DepartureCollection,
    response_model_by_alias=False,
)
async def departure_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    departureKind: icarEnums.icarDepartureKindType | None = None,
    departureReason: icarEnums.icarDepartureReasonType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a departure event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "departureKind": departureKind,
        "departureReason": departureReason,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.departure, query)
    return DepartureCollection(departure=result)
