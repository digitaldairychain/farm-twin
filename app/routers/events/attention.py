"""
Collects API calls related to animal attention events.

The attention of animals may be measured periodically by devices stationed
on the farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarAttentionEventResource.json
"""

from datetime import datetime
from typing import List

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ..ftCommon import dateBuild, filterQuery
from ..icar import icarEnums
from ..icar.icarResources import icarAttentionEventResource as Attention

router = APIRouter(
    prefix="/attention",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


class AttentionCollection(BaseModel):
    attention: List[Attention]


@router.post(
    "/",
    response_description="Add attention event",
    response_model=Attention,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_attention_event(request: Request, attention: Attention):
    """
    Create a new attention event.

    :param attention: Attention to be added
    """
    model = attention.model_dump(by_alias=True, exclude=["ft"])
    try:
        new_we = await request.app.state.attention.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=404, detail=f"Attention {attention} already exists"
        )
    if (
        created_attention_event := await request.app.state.attention.find_one(
            {"_id": new_we.inserted_id}
        )
    ) is not None:
        return created_attention_event
    raise HTTPException(
        status_code=404, detail="Attention event not successfully" + " added"
    )


@router.delete("/{ft}", response_description="Delete a attention event")
async def remove_attention_event(request: Request, ft: str):
    """
    Delete an attention event.

    :param ft: ObjectID of the attention event to delete
    """
    delete_result = await request.app.state.attention.delete_one({"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Attention event {ft} not found")


@router.get(
    "/",
    response_description="Search for attention event",
    response_model=AttentionCollection,
    response_model_by_alias=False,
)
async def attention_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    alertEndDateTimeStart: datetime | None = None,
    alertEndDateTimeEnd: datetime | None = None,
    category: icarEnums.icarAttentionCategoryType | None = None,
    cause: icarEnums.icarAttentionCauseType | None = None,
    priority: icarEnums.icarAttentionPriorityType | None = None,
    severity: icarEnums.icarDiagnosisSeverityType | None = None,
    deviceAttentionScore: int | None = None,
    device: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for an attention event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "alertEndDateTime": dateBuild(alertEndDateTimeStart, alertEndDateTimeEnd),
        "category": category,
        "causes": {"$in": cause},
        "priority": priority,
        "severity": severity,
        "deviceAttentionScore": deviceAttentionScore,
        "device.id": device,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await request.app.state.attention.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return AttentionCollection(attention=result)
    raise HTTPException(status_code=404, detail="No match found")
