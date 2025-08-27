"""
Collects API calls related to animal attention events.

The attention of animals may be measured periodically by devices stationed
on the farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarAttentionEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ..ftCommon import add_one_to_db, dateBuild, delete_one_from_db, find_in_db
from ..icar import icarEnums
from ..icar.icarResources import icarAttentionEventResource as Attention

router = APIRouter(
    prefix="/attention",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Attention"


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
    return await add_one_to_db(attention, request.app.state.attention, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete a attention event")
async def remove_attention_event(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete an attention event.

    :param ft: ObjectID of the attention event to delete
    """
    return await delete_one_from_db(request.app.state.attention, ft, ERROR_MSG_OBJECT)


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
    source: str | None = None,
    sourceId: str | None = None
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
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId
    }
    result = await find_in_db(request.app.state.attention, query)
    return AttentionCollection(attention=result)
