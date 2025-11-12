"""
Collects API calls related to animal death events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.5.0 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.5.0/resources/icarMovementDeathEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
)
from ...icar import icarEnums
from ...icar.icarResources import icarMovementDeathEventResource as Death
from ...users import User, get_current_active_user

ERROR_MSG_OBJECT = "Death"

router = APIRouter(
    prefix="/death",
    tags=["movement"],
    responses={404: {"description": "Not found"}},
)


class DeathCollection(BaseModel):
    death: List[Death]


@router.post(
    "/",
    response_description="Add death event",
    response_model=Death,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_death_event(
    request: Request,
    death: Death,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_movement"])
    ],
):
    """
    Create a new death event.

    :param death: Death to be added
    """
    return await add_one_to_db(
        death, request.app.state.death, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_death_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_movement"])
    ],
):
    """
    Delete a death event.

    :param ft: ObjectID of the death event to delete
    """
    return await delete_one_from_db(
        request.app.state.death, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for death event",
    response_model=DeathCollection,
    response_model_by_alias=False,
)
async def death_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_movement"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    deathReason: icarEnums.icarDeathReasonType | None = None,
    explanation: str | None = None,
    disposalMethod: icarEnums.icarDeathDisposalMethodType | None = None,
    disposalOperator: str | None = None,
    disposalReference: str | None = None,
    deathMethod: icarEnums.icarDeathMethodType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a death event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "deathReason": deathReason,
        "explanation": explanation,
        "disposalMethod": disposalMethod,
        "disposalOperator": disposalOperator,
        "disposalReference": disposalReference,
        "deathMethod": deathMethod,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.death, query)
    return DeathCollection(death=result)
