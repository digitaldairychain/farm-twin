"""
Collects API calls related to animal milking visit events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarMilkingVisitEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar import icarEnums
from ...icar.icarResources import icarMilkingVisitEventResource as Visit

ERROR_MSG_OBJECT = "Milking Visit"

router = APIRouter(
    prefix="/visit",
    tags=["events", "milking"],
    responses={404: {"description": "Not found"}},
)


class VisitCollection(BaseModel):
    visit: List[Visit]


@router.post(
    "/",
    response_description="Add milking visit event",
    response_model=Visit,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_visit_event(request: Request, visit: Visit):
    """
    Create a new milking visit event.

    :param visit: Visit to be added
    """
    model = visit.model_dump(by_alias=True, exclude=["ft"])
    return await add_one_to_db(model, request.app.state.visit, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_visit_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a milking visit event.

    :param ft: ObjectID of the visit event to delete
    """
    return await delete_one_from_db(request.app.state.visit, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for visit event",
    response_model=VisitCollection,
    response_model_by_alias=False,
)
async def visit_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    milkingStartingDateTimeStart: datetime | None = None,
    milkingStartingDateTimeEnd: datetime | None = None,
    milkingType: icarEnums.icarMilkingTypeCode | None = None,
    milkingComplete: bool | None = None,
    milkingParlourUnit: str | None = None,
    milkingBoxNumber: str | None = None,
    milkingDeviceId: str | None = None,
    measureDeviceId: str | None = None,
    milkingShiftLocalStartDateStart: datetime | None = None,
    milkingShiftLocalStartDateEnd: datetime | None = None,
    milkingShiftNumber: int | None = None,
):
    """Search for a milking visit event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "milkingStartingDateTime": dateBuild(
            milkingStartingDateTimeStart, milkingStartingDateTimeEnd
        ),
        "milkingType": milkingType,
        "milkingComplete": milkingComplete,
        "milkingParlourUnit": milkingParlourUnit,
        "milkingBoxNumber": milkingBoxNumber,
        "milkingDeviceId": milkingDeviceId,
        "measureDeviceId": measureDeviceId,
        "milkingShiftLocalStartDate": dateBuild(
            milkingShiftLocalStartDateStart, milkingShiftLocalStartDateEnd
        ),
        "milkingShiftNumber": milkingShiftNumber,
    }
    result = await find_in_db(request.app.state.visit, query)
    return VisitCollection(visit=result)
