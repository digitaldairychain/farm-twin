"""
Collects API calls related to animal feed intake events.

The duration and consumption of feed by animals may be periodically recorded
across a farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarFeedIntakeEventResource.json
"""

from datetime import datetime
from typing import List

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import dateBuild, filterQuery
from ...icar.icarResources import icarFeedIntakeEventResource as FeedIntake

router = APIRouter(
    prefix="/feed_intake",
    tags=["events", "feeding"],
    responses={404: {"description": "Not found"}},
)


class FeedIntakeCollection(BaseModel):
    feed_intake: List[FeedIntake]


@router.post(
    "/",
    response_description="Add feedintake event",
    response_model=FeedIntake,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_feed_intake_event(request: Request, feedintake: FeedIntake):
    """
    Create a new feed intake event.

    :param feedintake: Feed intake to be added
    """
    model = feedintake.model_dump(by_alias=True, exclude=["ft"])
    try:
        new_fie = await request.app.state.feed_intake.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404, detail="Feed intake already exists")
    if (
        created_feedintake_event := await request.app.state.feed_intake.find_one(
            {"_id": new_fie.inserted_id}
        )
    ) is not None:
        return created_feedintake_event
    raise HTTPException(
        status_code=404, detail="Feed intake event not successfully" + " added"
    )


@router.delete("/{ft}", response_description="Delete a feed intake event")
async def remove_feed_intake_event(request: Request, ft: str):
    """
    Delete a feed intake event.

    :param ft: ObjectID of the feed intake event to delete
    """
    delete_result = await request.app.state.feed_intake.delete_one(
        {"_id": ObjectId(ft)}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Feed intake event {ft} not found")


@router.get(
    "/",
    response_description="Search for feed intake event",
    response_model=FeedIntakeCollection,
    response_model_by_alias=False,
)
async def feed_intake_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    device: str | None = None,
    feedingStartingDateTimeStart: datetime | None = None,
    feedingStartingDateTimeEnd: datetime | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a feed intake event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "device.id": device,
        "feedingStartingDateTime": dateBuild(
            feedingStartingDateTimeStart, feedingStartingDateTimeEnd
        ),
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await request.app.state.feed_intake.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return FeedIntakeCollection(feed_intake=result)
    raise HTTPException(status_code=404, detail="No match found")
