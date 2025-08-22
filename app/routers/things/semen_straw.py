"""
Collects API calls related to semen straws.

This collection of endpoints allows for the addition, deletion
and finding of semen straws.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ..ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                        find_in_db, update_one_in_db)
from ..icar import icarEnums
from ..icar.icarResources import icarReproSemenStrawResource as SemenStraw

router = APIRouter(
    prefix="/semen_straw",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Semen Straw"


class SemenStrawCollection(BaseModel):
    semen_straw: List[SemenStraw]


@router.post(
    "/",
    response_description="Add new semen straw",
    response_model=SemenStraw,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_semen_straw(request: Request, semen_straw: SemenStraw):
    """
    Create a new semen straw.

    :param semen_straw: SemenStraw to be added
    """
    model = semen_straw.model_dump(by_alias=True, exclude=["ft", "resourceType"])
    return await add_one_to_db(model, request.app.state.semen_straw, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete an semen straw")
async def remove_semen_straw(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a semen straw.

    :param ft: UUID of the semen straw to delete
    """
    return await delete_one_from_db(request.app.state.semen_straw, ft, ERROR_MSG_OBJECT)


@router.patch(
    "/{ft}",
    response_description="Update an semen straw",
    response_model=SemenStraw,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_semen_straw(
    request: Request, ft: mongo_object_id.MongoObjectId, semen_straw: SemenStraw
):
    """
    Update an existing semen straw if it exists.

    :param ft: UUID of the semen straw to update
    :param semen_straw: SemenStraw to update with
    """
    return await update_one_in_db(
        semen_straw, request.app.state.semen_straw, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for an semen straw",
    response_model=SemenStrawCollection,
    response_model_by_alias=False,
)
async def semen_straw_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    id: str | None = None,
    batch: str | None = None,
    collectionCentre: str | None = None,
    dateCollected: datetime | None = None,
    sireOfficialName: str | None = None,
    sireURI: str | None = None,
    preservationType: icarEnums.icarReproSemenPreservationType | None = None,
    isSexedSemen: bool | None = None,
    sexedGender: icarEnums.icarAnimalGenderType | None = None,
    sexedPercentage: int | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
):
    """Search for a semen straw given the provided criteria."""
    query = {
        "_id": ft,
        "id": id,
        "batch": batch,
        "collectionCentre": collectionCentre,
        "dateCollected": dateCollected,
        "sireOfficialName": sireOfficialName,
        "sireURI": sireURI,
        "preservationType": preservationType,
        "isSexedSemen": isSexedSemen,
        "sexedGender": sexedGender,
        "sexedPercentage": sexedPercentage,
        "modified": dateBuild(modifiedStart, modifiedEnd),
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.semen_straw, query)
    return SemenStrawCollection(semen_straw=result)
