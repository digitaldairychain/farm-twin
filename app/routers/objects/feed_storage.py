"""
Collects API calls related to feed storage.

This collection of endpoints allows for the addition, deletion
and finding of feed storages.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ..ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                        find_in_db, update_one_in_db)
from ..icar.icarResources import icarFeedStorageResource as FeedStorage

router = APIRouter(
    prefix="/feed_storage",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Feed Storage"


class FeedStorageCollection(BaseModel):
    feed_storage: List[FeedStorage]


@router.post(
    "/",
    response_description="Add new feed storage",
    response_model=FeedStorage,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_feed_storage(request: Request, feed_storage: FeedStorage):
    """
    Create a new feed storage.

    :param feed_storage: Feed Storage to be added
    """
    return await add_one_to_db(
        feed_storage, request.app.state.feed_storage, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a feed storage")
async def remove_feed_storage(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a feed storage.

    :param ft: UUID of the feed storage to delete
    """
    return await delete_one_from_db(
        request.app.state.feed_storage, ft, ERROR_MSG_OBJECT
    )


@router.patch(
    "/{ft}",
    response_description="Update a feed_storage",
    response_model=FeedStorage,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_feed_storage(
    request: Request, ft: mongo_object_id.MongoObjectId, feed_storage: FeedStorage
):
    """
    Update an existing feed_storage if it exists.

    :param ft: UUID of the feed_storage to update
    :param feed_storage: Feed Storage to update with
    """
    return await update_one_in_db(
        feed_storage, request.app.state.feed_storage, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for feed_storage",
    response_model=FeedStorageCollection,
    response_model_by_alias=False,
)
async def feed_storage_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    id: str | None = None,
    serial: str | None = None,
    name: str | None = None,
    description: str | None = None,
    softwareVersion: str | None = None,
    hardwareVersion: str | None = None,
    isActive: bool | None = None,
    feedId: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
):
    """Search for a feed_storage given the provided criteria."""
    query = {
        "_id": ft,
        "id": id,
        "serial": serial,
        "name": name,
        "description": description,
        "softwareVersion": softwareVersion,
        "hardwareVersion": hardwareVersion,
        "isActive": isActive,
        "feedId": feedId,
        "modified": dateBuild(modifiedStart, modifiedEnd),
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.feed_storage, query)
    return FeedStorageCollection(feed_storage=result)
