"""
Collects API calls related to animal arrival events.

The duration and consumption of feed by animals may be periodically recorded
across a farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarMovementArrivalEventResource.json
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import dateBuild, filterQuery, delete_one_from_db, add_one_to_db
from ...icar import icarEnums, icarTypes
from ..eventCommon import AnimalEventModel

ERROR_MSG_OBJECT = "Arrival"

router = APIRouter(
    prefix="/arrival",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)


class Arrival(AnimalEventModel):
    arrivalReason: Optional[icarEnums.icarArrivalReasonType] = Field(
        default=None,
        json_schema_extra={
            "description": "Reason the animal arrived on the holding.",
        },
    )
    animalState: Optional[icarTypes.icarAnimalStateType] = Field(
        default=None,
        json_schema_extra={
            "description": "State information about an animal.",
        },
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the consignment of the animal to the holding.",
        },
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
    return await add_one_to_db(
        model, request.app.state.arrival, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description=f"Delete event")
async def remove_arrival_event(request: Request,
                               ft: mongo_object_id.MongoObjectId):
    """
    Delete a arrival event.

    :param ft: ObjectID of the arrival event to delete
    """
    return await delete_one_from_db(
        request.app.state.arrival, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for arrival event",
    response_model=ArrivalCollection,
    response_model_by_alias=False,
)
async def arrival_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: mongo_object_id.MongoObjectId | None = None,
    arrivalReason: icarEnums.icarArrivalReasonType | None = None,
    currentLactationParity: int | None = None,
    lastCalvingDateStart: datetime | None = None,
    lastCalvingDateEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
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
        "animal": animal,
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
    result = await request.app.state.arrival.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return ArrivalCollection(arrival=result)
    raise HTTPException(status_code=404, detail="No match found")
