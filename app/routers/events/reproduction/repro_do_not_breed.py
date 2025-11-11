"""
Collects API calls related to animal repro DNB events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarReproDoNotBreedEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import add_one_to_db, dateBuild, delete_one_from_db, find_in_db
from ...icar.icarResources import icarReproDoNotBreedEventResource as ReproDNB
from ...users import User, get_current_active_user

ERROR_MSG_OBJECT = "Repro DNB"

router = APIRouter(
    prefix="/repro_do_not_breed",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproDNBCollection(BaseModel):
    repro_do_not_breed: List[ReproDNB]


@router.post(
    "/",
    response_description="Add repro DNB event",
    response_model=ReproDNB,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_dnb_event(
    request: Request,
    repro_dnb: ReproDNB,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_reproduction"])
    ],
):
    """
    Create a new repro DNB event.

    :param repro_dnb: Repro DNB to be added
    """
    return await add_one_to_db(
        repro_dnb, request.app.state.repro_do_not_breed, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_dnb_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_reproduction"])
    ],
):
    """
    Delete a repro DNB event.

    :param ft: ObjectID of the repro DNB event to delete
    """
    return await delete_one_from_db(
        request.app.state.repro_do_not_breed, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for repro DNB event",
    response_model=ReproDNBCollection,
    response_model_by_alias=False,
)
async def repro_dnb_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_reproduction"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    doNotBreed: bool | None = True,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a repro DNB event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "doNotBreed": doNotBreed,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.repro_do_not_breed, query)
    return ReproDNBCollection(repro_do_not_breed=result)
