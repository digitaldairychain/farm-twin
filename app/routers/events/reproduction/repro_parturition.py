"""
Collects API calls related to animal repro parturition events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarReproParturitionEventResource.json
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
    icarReproParturitionEventResource as ReproParturition

ERROR_MSG_OBJECT = "Repro Parturition"

router = APIRouter(
    prefix="/repro_parturition",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproParturitionCollection(BaseModel):
    repro_parturition: List[ReproParturition]


@router.post(
    "/",
    response_description="Add repro parturition event",
    response_model=ReproParturition,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_parturition_event(
    request: Request, repro_parturition: ReproParturition
):
    """
    Create a new repro parturition event.

    :param repro_parturition: Repro Parturition to be added
    """
    model = repro_parturition.model_dump(by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(
        model, request.app.state.repro_parturition, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_parturition_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a repro_parturition event.

    :param ft: ObjectID of the repro parturition event to delete
    """
    return await delete_one_from_db(
        request.app.state.repro_parturition, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for repro parturition event",
    response_model=ReproParturitionCollection,
    response_model_by_alias=False,
)
async def repro_parturition_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    isEmbryoImplant: bool | None = None,
    damParity: int | None = None,
    liveProgeny: int | None = None,
    totalProgeny: int | None = None,
    calvingEase: icarEnums.icarReproCalvingEaseType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a repro parturition event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "isEmbryoImplant": isEmbryoImplant,
        "damParity": damParity,
        "liveProgeny": liveProgeny,
        "totalProgeny": totalProgeny,
        "calvingEase": calvingEase,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.repro_parturition, query)
    return ReproParturitionCollection(repro_parturition=result)
