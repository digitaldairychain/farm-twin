"""
Collects API calls related to animal repro abortion events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarReproAbortionEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar.icarResources import \
    icarReproAbortionEventResource as ReproAbortion

ERROR_MSG_OBJECT = "Repro Abortion"

router = APIRouter(
    prefix="/repro_abortion",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproAbortionCollection(BaseModel):
    repro_abortion: List[ReproAbortion]


@router.post(
    "/",
    response_description="Add repro abortion event",
    response_model=ReproAbortion,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_abortion_event(request: Request, repro_abortion: ReproAbortion):
    """
    Create a new repro abortion event.

    :param repro_abortion: Repro Abortion to be added
    """
    return await add_one_to_db(
        repro_abortion, request.app.state.repro_abortion, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_abortion_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a repro_abortion event.

    :param ft: ObjectID of the repro abortion event to delete
    """
    return await delete_one_from_db(
        request.app.state.repro_abortion, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for repro abortion event",
    response_model=ReproAbortionCollection,
    response_model_by_alias=False,
)
async def repro_abortion_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None
):
    """Search for a repro abortion event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId
    }
    result = await find_in_db(request.app.state.repro_abortion, query)
    return ReproAbortionCollection(repro_abortion=result)
