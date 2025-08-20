"""
Collects API calls related to animal repro insemination events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarReproInseminationEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar.icarResources import \
    icarReproInseminationEventResource as ReproInsemination

ERROR_MSG_OBJECT = "Repro Insemination"

router = APIRouter(
    prefix="/repro_insemination",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproInseminationCollection(BaseModel):
    repro_insemination: List[ReproInsemination]


@router.post(
    "/",
    response_description="Add repro insemination event",
    response_model=ReproInsemination,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_insemination_event(
    request: Request, repro_insemination: ReproInsemination
):
    """
    Create a new repro insemination event.

    :param repro_insemination: Repro Insemination to be added
    """
    model = repro_insemination.model_dump(
        by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(
        model, request.app.state.repro_insemination, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_insemination_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a repro_insemination event.

    :param ft: ObjectID of the repro insemination event to delete
    """
    return await delete_one_from_db(
        request.app.state.repro_insemination, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for repro insemination event",
    response_model=ReproInseminationCollection,
    response_model_by_alias=False,
)
async def repro_insemination_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a repro insemination event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.repro_insemination, query)
    return ReproInseminationCollection(repro_insemination=result)
