"""
Collects API calls related to animal arrival events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarMovementArrivalEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Query, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar import icarEnums
from ...icar.icarResources import icarMovementArrivalEventResource as Arrival

ERROR_MSG_OBJECT = "Arrival"

router = APIRouter(
    prefix="/arrival",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)


class ArrivalCollection(BaseModel):
    arrival: List[Arrival]


@router.post(
    "/",
    response_description="Add arrival event",
    response_model=Arrival,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_arrival_event(request: Request, arrival: Arrival):
    """
    Create a new arrival event.

    :param arrival: Arrival to be added
    """
    model = arrival.model_dump(by_alias=True, exclude=["ft"])
    return await add_one_to_db(model, request.app.state.arrival, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_arrival_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a arrival event.

    :param ft: ObjectID of the arrival event to delete
    """
    return await delete_one_from_db(request.app.state.arrival, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for arrival event",
    response_model=ArrivalCollection,
    response_model_by_alias=False,
)
async def arrival_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    arrivalReason: icarEnums.icarArrivalReasonType | None = None,
    currentLactationParity: int | None = None,
    lastCalvingDateStart: datetime | None = None,
    lastCalvingDateEnd: Annotated[datetime, Query(default_factory=datetime.now)] = None,
    lastInseminationDateStart: datetime | None = None,
    lastInseminationDateEnd: datetime | None = None,
    lastDryingOffDateStart: datetime | None = None,
    lastDryingOffDateEnd: datetime | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a arrival event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "arrivalReason": arrivalReason,
        "animalState.currentLactationParity": currentLactationParity,
        "animalState.lastCalvingDate": dateBuild(
            lastCalvingDateStart, lastCalvingDateEnd
        ),
        "animalState.lastInseminationDate": dateBuild(
            lastInseminationDateStart, lastInseminationDateEnd
        ),
        "animalState.lastDryingOffDate": dateBuild(
            lastDryingOffDateStart, lastDryingOffDateEnd
        ),
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.arrival, query)
    return ArrivalCollection(arrival=result)
