"""
Collects API calls related to location.

This collection of endpoints allows for the addition, deletion
and finding of locations.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Query, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
    update_one_in_db,
)
from ..icar import icarTypes
from ..icar.icarResources import icarLocationResource as Location
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/location",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Location"


class LocationCollection(BaseModel):
    location: List[Location]


@router.post(
    "/",
    response_description="Add new location",
    response_model=Location,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_location(
    request: Request,
    location: Location,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_location"])
    ],
):
    """
    Create a new location.

    :param location: Location to be added
    """
    return await add_one_to_db(
        location, request.app.state.location, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a location")
async def remove_location(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_location"])
    ],
):
    """
    Delete a location.

    :param ft: UUID of the location to delete
    """
    return await delete_one_from_db(
        request.app.state.location, ft, ERROR_MSG_OBJECT
    )


@router.patch(
    "/{ft}",
    response_description="Update a location",
    response_model=Location,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_location(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    location: Location,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_location"])
    ],
):
    """
    Update an existing location if it exists.

    :param ft: UUID of the location to update
    :param location: Location to update with
    """
    return await update_one_in_db(
        location, request.app.state.location, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for location",
    response_model=LocationCollection,
    response_model_by_alias=False,
)
async def location_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_location"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    identifier: icarTypes.icarAnimalIdentifierType | None = None,
    alternativeIdentifiers: Annotated[list[str] | None, Query()] = [],
    name: str | None = None,
    timeZoneId: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a location given the provided criteria."""
    query = {
        "_id": ft,
        "identifier": identifier,
        "alternativeIdentifiers": {"$in": alternativeIdentifiers},
        "name": name,
        "timeZoneId": timeZoneId,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.modified": dateBuild(modifiedStart, modifiedEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.location, query)
    return LocationCollection(location=result)
