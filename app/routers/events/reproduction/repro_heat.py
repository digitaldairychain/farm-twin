"""
Collects API calls related to animal repro heat events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarReproHeatEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar import icarEnums
from ...icar.icarResources import icarReproHeatEventResource as ReproHeat

ERROR_MSG_OBJECT = "Repro Heat"

router = APIRouter(
    prefix="/repro_heat",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproHeatCollection(BaseModel):
    repro_heat: List[ReproHeat]


@router.post(
    "/",
    response_description="Add repro heat event",
    response_model=ReproHeat,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_heat_event(request: Request, repro_heat: ReproHeat):
    """
    Create a new repro heat event.

    :param repro_heat: Repro Heat to be added
    """
    model = repro_heat.model_dump(
        by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(model, request.app.state.repro_heat, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_heat_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a repro_heat event.

    :param ft: ObjectID of the repro heat event to delete
    """
    return await delete_one_from_db(request.app.state.repro_heat, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for repro heat event",
    response_model=ReproHeatCollection,
    response_model_by_alias=False,
)
async def repro_heat_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    heatDetectionMethod: icarEnums.icarReproHeatDetectionMethodType | None = None,
    commencementDateTime: datetime | None = None,
    expirationDateTime: datetime | None = None,
    deviceHeatProbability: int | None = None,
    device: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a repro heat event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "heatDetectionMethod": heatDetectionMethod,
        "commencementDateTime": commencementDateTime,
        "expirationDateTime": expirationDateTime,
        "deviceHeatProbability": deviceHeatProbability,
        "device.id": device,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.repro_heat, query)
    return ReproHeatCollection(repro_heat=result)
