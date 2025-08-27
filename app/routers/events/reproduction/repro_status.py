"""
Collects API calls related to animal repro status events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarReproStatusObservedEventResource.json
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
    icarReproStatusObservedEventResource as ReproStatus

ERROR_MSG_OBJECT = "Repro Status"

router = APIRouter(
    prefix="/repro_status",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproStatusCollection(BaseModel):
    repro_status: List[ReproStatus]


@router.post(
    "/",
    response_description="Add repro status event",
    response_model=ReproStatus,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_status_event(request: Request, repro_status: ReproStatus):
    """
    Create a new repro status event.

    :param repro_status: Repro Status to be added
    """
    return await add_one_to_db(
        repro_status, request.app.state.repro_status, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_status_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a repro_status event.

    :param ft: ObjectID of the repro status event to delete
    """
    return await delete_one_from_db(
        request.app.state.repro_status, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for repro status event",
    response_model=ReproStatusCollection,
    response_model_by_alias=False,
)
async def repro_status_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    observedStatus: icarEnums.icarAnimalReproductionStatusType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None
):
    """Search for a repro status event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "observedStatus": observedStatus,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId
    }
    result = await find_in_db(request.app.state.repro_status, query)
    return ReproStatusCollection(repro_status=result)
