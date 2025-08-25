"""
Collects API calls related to animal observation events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarCarcassObservationsEventResource.json
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
    icarCarcassObservationsEventResource as Carcass

ERROR_MSG_OBJECT = "Carcass"

router = APIRouter(
    prefix="/carcass",
    tags=["observations"],
    responses={404: {"description": "Not found"}},
)


class CarcassCollection(BaseModel):
    carcass: List[Carcass]


@router.post(
    "/",
    response_description="Add carcass event",
    response_model=Carcass,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_carcass_event(request: Request, carcass: Carcass):
    """
    Create a new carcass event.

    :param carcass: Carcass to be added
    """
    return await add_one_to_db(carcass, request.app.state.carcass, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete event")
async def remove_carcass_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a carcass event.

    :param ft: ObjectID of the carcass event to delete
    """
    return await delete_one_from_db(request.app.state.carcass, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for carcass event",
    response_model=CarcassCollection,
    response_model_by_alias=False,
)
async def carcass_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    side: icarEnums.icarCarcassSideType | None = None,
    primal: icarEnums.icarCarcassPrimalType | None = None,
    carcassState: icarEnums.icarCarcassStateType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a carcass event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "side": side,
        "primal": primal,
        "carcassState": carcassState,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.carcass, query)
    return CarcassCollection(carcass=result)
