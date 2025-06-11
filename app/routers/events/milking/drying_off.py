"""
Collects API calls related to drying off of animals in milk.

Records that the animal has been dried off from milking.
If necessary, also record a separate health treatment event.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarMilkingDryOffEventResource.json
"""
from datetime import datetime
from typing import List

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import filterQuery
from ..eventCommon import AnimalEventModel

router = APIRouter(
    prefix="/drying_off",
    tags=["events", "milking"],
    responses={404: {"description": "Not found"}},
)


class DryingOff(AnimalEventModel):
    pass


class DryingOffCollection(BaseModel):
    drying_off: List[DryingOff]


@router.post(
    "/",
    response_description="Add drying off event",
    response_model=DryingOff,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_drying_off_event(request: Request, dryingoff: DryingOff):
    """
    Create a new drying off event.

    :param dryingoff: Drying off to be added
    """
    model = dryingoff.model_dump(by_alias=True, exclude=["ft"])
    try:
        new_fie = await request.app.state.drying_off.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail="Drying off already exists")
    if (
        created_dryingoff_event :=
        await request.app.state.drying_off.find_one(
            {"_id": new_fie.inserted_id}
        )
    ) is not None:
        return created_dryingoff_event
    raise HTTPException(
        status_code=404, detail="Drying off event not successfully" + " added"
    )


@router.delete("/{ft}", response_description="Delete a drying off event")
async def remove_drying_off_event(request: Request, ft: str):
    """
    Delete a drying off event.

    :param ft: ObjectID of the drying off event to delete
    """
    delete_result = await request.app.state.drying_off.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"Drying off event {ft} not found")


@router.get(
    "/",
    response_description="Search for drying off event",
    response_model=DryingOffCollection,
    response_model_by_alias=False,
)
async def drying_off_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: mongo_object_id.MongoObjectId | None = None,
    createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
):
    """Search for a drying off event given the provided criteria."""
    query = {
        "_id": ft,
        "animal": animal,
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": createdStart, "$lte": createdEnd},
    }
    result = await request.app.state.drying_off.find(
        filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return DryingOffCollection(drying_off=result)
    raise HTTPException(status_code=404, detail="No match found")
