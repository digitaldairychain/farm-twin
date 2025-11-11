"""
Collects API calls related to conformation events.

A conformation resource used to indicate that product should be separated
(e.g. colostrum from newly lactating cows).

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarConformationScoreEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import add_one_to_db, dateBuild, delete_one_from_db, find_in_db
from ...icar.icarResources import icarConformationScoreEventResource as Conformation
from ...users import User, get_current_active_user

router = APIRouter(
    prefix="/conformation",
    tags=["performance"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Conformation"


class ConformationCollection(BaseModel):
    conformation: List[Conformation]


@router.post(
    "/",
    response_description="Add conformation event",
    response_model=Conformation,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_conformation_event(
    request: Request,
    conformation: Conformation,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_performance"])
    ],
):
    """
    Create a new conformation event.

    :param conformation: Conformation to be added
    """
    return await add_one_to_db(
        conformation, request.app.state.conformation, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a conformation event")
async def remove_conformation_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_performance"])
    ],
):
    """
    Delete a conformation event.

    :param ft: ObjectID of the conformation event to delete
    """
    return await delete_one_from_db(
        request.app.state.conformation, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for conformation event",
    response_model=ConformationCollection,
    response_model_by_alias=False,
)
async def conformation_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_performance"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a conformation event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.conformation, query)
    return ConformationCollection(conformation=result)
