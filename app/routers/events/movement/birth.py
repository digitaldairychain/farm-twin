"""
Collects API calls related to animal birth events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarMovementBirthEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar import icarEnums
from ...icar.icarResources import icarMovementBirthEventResource as Birth

ERROR_MSG_OBJECT = "Birth"

router = APIRouter(
    prefix="/birth",
    tags=["movement"],
    responses={404: {"description": "Not found"}},
)


class BirthCollection(BaseModel):
    birth: List[Birth]


@router.post(
    "/",
    response_description="Add birth event",
    response_model=Birth,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_birth_event(request: Request, birth: Birth):
    """
    Create a new birth event.

    :param birth: Birth to be added
    """
    return await add_one_to_db(birth, request.app.state.birth, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_birth_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a birth event.

    :param ft: ObjectID of the birth event to delete
    """
    return await delete_one_from_db(request.app.state.birth, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for birth event",
    response_model=BirthCollection,
    response_model_by_alias=False,
)
async def birth_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    registrationReason: icarEnums.icarRegistrationReasonType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None
):
    """Search for a birth event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "registrationReason": registrationReason,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId
    }
    result = await find_in_db(request.app.state.birth, query)
    return BirthCollection(birth=result)
