"""
Collects API calls related to feed.

This collection of endpoints allows for the addition, deletion
and finding of feeds.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
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
from ..icar import icarEnums
from ..icar.icarResources import icarFeedResource as Feed
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/feed",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Feed"


class FeedCollection(BaseModel):
    feed: List[Feed]


@router.post(
    "/",
    response_description="Add new feed",
    response_model=Feed,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_feed(
    request: Request,
    feed: Feed,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_feed"])
    ],
):
    """
    Create a new feed.

    :param feed: Feed to be added
    """
    return await add_one_to_db(feed, request.app.state.feed, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete a feed")
async def remove_feed(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_feed"])
    ],
):
    """
    Delete a feed.

    :param ft: UUID of the feed to delete
    """
    return await delete_one_from_db(request.app.state.feed, ft, ERROR_MSG_OBJECT)


@router.patch(
    "/{ft}",
    response_description="Update a feed",
    response_model=Feed,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_feed(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    feed: Feed,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_feed"])
    ],
):
    """
    Update an existing feed if it exists.

    :param ft: UUID of the feed to update
    :param feed: Feed to update with
    """
    return await update_one_in_db(feed, request.app.state.feed, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for feed",
    response_model=FeedCollection,
    response_model_by_alias=False,
)
async def feed_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_feed"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    id: str | None = None,
    category: icarEnums.icarFeedCategoryType | None = None,
    type: str | None = None,
    name: str | None = None,
    active: bool | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a feed given the provided criteria."""
    query = {
        "_id": ft,
        "id": id,
        "category": category,
        "type.id": type,
        "name": name,
        "active": active,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.modified": dateBuild(modifiedStart, modifiedEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.feed, query)
    return FeedCollection(feed=result)
