"""
Collects API calls related to conformation events.

A conformation resource used to indicate that product should be separated
(e.g. colostrum from newly lactating cows).

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarConformationScoreEventResource.json
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from ..ftCommon import dateBuild, filterQuery
from ..icar import icarEnums
from ..icar.icarResources import icarConformationScoreEventResource as Conformation

router = APIRouter(
    prefix="/conformation",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


class ConformationCollection(BaseModel):
    conformation: List[Conformation]


@router.post(
    "/",
    response_description="Add conformation event",
    response_model=Conformation,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_conformation_event(request: Request, conformation: Conformation):
    """
    Create a new conformation event.

    :param conformation: Conformation to be added
    """
    model = conformation.model_dump(by_alias=True, exclude=["ft"])
    try:
        new_ce = await request.app.state.conformation.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=404, detail="Conformation event already exists")
    if (
        created_conformation_event := await request.app.state.conformation.find_one(
            {"_id": new_ce.inserted_id}
        )
    ) is not None:
        return created_conformation_event
    raise HTTPException(
        status_code=404, detail="Conformation event not successfully added"
    )


@router.delete("/{ft}", response_description="Delete a conformation event")
async def remove_conformation_event(request: Request, ft: str):
    """
    Delete a conformation event.

    :param ft: ObjectID of the conformation event to delete
    """
    delete_result = await request.app.state.conformation.delete_one(
        {"_id": ObjectId(ft)}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"Conformation event {ft} not found")


@router.get(
    "/",
    response_description="Search for conformation event",
    response_model=ConformationCollection,
    response_model_by_alias=False,
)
async def conformation_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
):
    """Search for a conformation event given the provided criteria."""
    query = {
        "_id": ft,
        "animal": {"id": animal}
    }
    result = await request.app.state.conformation.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return ConformationCollection(conformation=result)
    raise HTTPException(status_code=404, detail="No match found")
