"""
Collects API calls related to animal repro pregnancy_check events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarReproPregnancyCheckEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar.icarResources import \
    icarReproPregnancyCheckEventResource as ReproPregnancyCheck

ERROR_MSG_OBJECT = "Repro Pregnancy Check"

router = APIRouter(
    prefix="/repro_pregnancy_check",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproPregnancyCheckCollection(BaseModel):
    repro_pregnancy_check: List[ReproPregnancyCheck]


@router.post(
    "/",
    response_description="Add repro pregnancy check event",
    response_model=ReproPregnancyCheck,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_pregnancy_check_event(
    request: Request, repro_pregnancy_check: ReproPregnancyCheck
):
    """
    Create a new repro pregnancy check event.

    :param repro_pregnancy_check: Repro pregnancy check to be added
    """
    model = repro_pregnancy_check.model_dump(
        by_alias=True, exclude=["ft", "resourceType"]
    )
    return await add_one_to_db(
        model, request.app.state.repro_pregnancy_check, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_pregnancy_check_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a repro_pregnancy check event.

    :param ft: ObjectID of the repro pregnancy check event to delete
    """
    return await delete_one_from_db(
        request.app.state.repro_pregnancy_check, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for repro pregnancy check event",
    response_model=ReproPregnancyCheckCollection,
    response_model_by_alias=False,
)
async def repro_pregnancy_check_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a repro pregnancy check event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.repro_pregnancy_check, query)
    return ReproPregnancyCheckCollection(repro_pregnancy_check=result)
