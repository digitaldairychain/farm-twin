"""
Collects API calls related to animal death events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarMovementDeathEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar import icarEnums
from ...icar.icarResources import icarMovementDeathEventResource as Death

ERROR_MSG_OBJECT = "Death"

router = APIRouter(
    prefix="/death",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)


class DeathCollection(BaseModel):
    death: List[Death]


@router.post(
    "/",
    response_description="Add death event",
    response_model=Death,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_death_event(request: Request, death: Death):
    """
    Create a new death event.

    :param death: Death to be added
    """
    model = death.model_dump(by_alias=True, exclude=["ft"])
    return await add_one_to_db(model, request.app.state.death, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_death_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a death event.

    :param ft: ObjectID of the death event to delete
    """
    return await delete_one_from_db(request.app.state.death, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for death event",
    response_model=DeathCollection,
    response_model_by_alias=False,
)
async def death_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    deathReason: icarEnums.icarDeathReasonType | None = None,
    explanation: str | None = None,
    disposalMethod: icarEnums.icarDeathDisposalMethodType | None = None,
    disposalOperator: str | None = None,
    disposalReference: str | None = None,
    deathMethod: icarEnums.icarDeathMethodType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a death event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "deathReason": deathReason,
        "explanation": explanation,
        "disposalMethod": disposalMethod,
        "disposalOperator": disposalOperator,
        "disposalReference": disposalReference,
        "deathMethod": deathMethod,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.death, query)
    return DeathCollection(death=result)
