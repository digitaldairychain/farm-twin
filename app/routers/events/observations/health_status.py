"""
Collects API calls related to animal health status events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarHealthStatusObservedEventResource.json
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
    icarHealthStatusObservedEventResource as HealthStatus

ERROR_MSG_OBJECT = "Health Status"

router = APIRouter(
    prefix="/health_status",
    tags=["observations", "health"],
    responses={404: {"description": "Not found"}},
)


class HealthStatusCollection(BaseModel):
    health_status: List[HealthStatus]


@router.post(
    "/",
    response_description="Add health status event",
    response_model=HealthStatus,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_health_status_event(request: Request, health_status: HealthStatus):
    """
    Create a new health status event.

    :param health_status: Health Status to be added
    """
    model = health_status.model_dump(by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(model, request.app.state.health_status, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_health_status_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a health_status event.

    :param ft: ObjectID of the health status event to delete
    """
    return await delete_one_from_db(
        request.app.state.health_status, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for health status event",
    response_model=HealthStatusCollection,
    response_model_by_alias=False,
)
async def health_status_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    observedStatus: icarEnums.icarAnimalHealthStatusType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a health status event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "observedStatus": observedStatus,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.health_status, query)
    return HealthStatusCollection(health_status=result)
