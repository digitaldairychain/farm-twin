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

from ...ftCommon import filterQuery
from ...icar import icarTypes, icarEnums
from ..eventCommon import AnimalEventModel

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
        }
    )
    animalState: Optional[icarTypes.icarAnimalStateType] = Field(
        default=None,
        json_schema_extra={
            "description": "State information about an animal.",
        }
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the consignment of the animal to the holding.",
        }
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
    try:
        new_ae = await request.app.state.arrival.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail="Arrival already exists")
    if (
        created_arrival_event :=
        await request.app.state.arrival.find_one(
            {"_id": new_ae.inserted_id}
        )
    ) is not None:
        return created_arrival_event
    raise HTTPException(
        status_code=404, detail="Arrival event not successfully" + " added"
    )
    # TODO: Is this common code?


@router.delete("/{ft}", response_description="Delete a arrival event")
async def remove_arrival_event(request: Request, ft: str):
    """
    Delete a arrival event.

    :param ft: ObjectID of the arrival event to delete
    """
    delete_result = await request.app.state.arrival.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"Arrival event {ft} not found")
    # TODO: Is this common code?


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
    lastCalvingDateStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    lastCalvingDateEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
    lastInsemintationDateStart: datetime | None = datetime(
        1970, 1, 1, 0, 0, 0),
    lastInsemintationDateEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
    lastDryingOffDateStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    lastDryingOffDateEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
    createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
):
    """Search for a arrival event given the provided criteria."""
    query = {
        "_id": ft,
        "animal": animal,
        "arrivalReason": arrivalReason,
        "animalState.currentLactationParity": currentLactationParity,
        "animalState.lastCalvingDate": {"$gte": lastCalvingDateStart, "$lte": lastCalvingDateEnd},
        "animalState.lastInseminationDate": {"$gte": lastInsemintationDateStart, "$lte": lastInsemintationDateEnd},
        "animalState.lastDryingOffDate": {"$gte": lastDryingOffDateStart, "$lte": lastDryingOffDateEnd},
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": createdStart, "$lte": createdEnd},
    }
    result = await request.app.state.arrival.find(
        filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return ArrivalCollection(arrival=result)
    raise HTTPException(status_code=404, detail="No match found")
