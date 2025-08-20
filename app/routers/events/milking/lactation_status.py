"""
Collects API calls related to lactation status based on observation.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarLactationStatusObservedEventResource.json
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
    icarLactationStatusObservedEventResource as LactationStatus

ERROR_MSG_OBJECT = "Lactation Status"

router = APIRouter(
    prefix="/lactation_status",
    tags=["milking"],
    responses={404: {"description": "Not found"}},
)


class LactationStatusCollection(BaseModel):
    lactation_status: List[LactationStatus]


@router.post(
    "/",
    response_description="Add lactation status event",
    response_model=LactationStatus,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_lactation_status_event(
    request: Request, lactation_status: LactationStatus
):
    """
    Create a new lactation status event.

    :param lactation_status: Lactation Status to be added
    """
    model = lactation_status.model_dump(
        by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(
        model, request.app.state.lactation_status, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_lactation_status_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a lactation_status event.

    :param ft: ObjectID of the lactation status event to delete
    """
    return await delete_one_from_db(
        request.app.state.lactation_status, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for lactation status event",
    response_model=LactationStatusCollection,
    response_model_by_alias=False,
)
async def lactation_status_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    observedStatus: icarEnums.icarAnimalLactationStatusType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a lactation status event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "observedStatus": observedStatus,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.lactation_status, query)
    return LactationStatusCollection(lactation_status=result)
